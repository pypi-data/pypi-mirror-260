from pms_inference_engine._const import *
from typing import List, Type, TypeVar
from pms_inference_engine._ray_processor import RayProcessor
from pms_inference_engine.interface import IEngineProcessor

__PROC_LIST = []


def register(__cls: Type[ProcessorTypeT]) -> Type[ProcessorTypeT]:
    assert issubclass(
        __cls, IEngineProcessor
    ), f"[{__cls}] is not subclass of {IEngineProcessor}"
    assert __cls not in __PROC_LIST, f"[{__cls}] is already registered."
    __PROC_LIST.append(__cls)
    return __cls


def __wrap_with_ray(target_class: type, **kwargs) -> RayProcessor:
    return RayProcessor(target_class=target_class, **kwargs)


def is_wrapped_ray(processor_type: str) -> bool:
    return processor_type.startswith(RAY_PROCESSOR_PREFIX)


def get_local_processor_type(processor_type: str) -> str:
    assert is_wrapped_ray(
        processor_type
    ), f"{processor_type} is not ray(remote) processor type"
    processor_type = processor_type.replace(RAY_PROCESSOR_PREFIX, "", 1)
    return processor_type


def is_valid_processor_type(processor_type: str) -> bool:
    processor_keys = [p.__name__ for p in __PROC_LIST]
    if is_wrapped_ray(processor_type):
        processor_type = get_local_processor_type(processor_type)
    return processor_type in processor_keys


def get_processor_types() -> List[str]:
    return [p.__name__ for p in __PROC_LIST]


def create_processor(
    processor_type: str,
    processor_idx: int,
    **kwargs,
) -> IEngineProcessor:
    assert is_valid_processor_type(
        processor_type
    ), f"'{processor_type}' is wrong processor type."
    kwargs["index"] = processor_idx
    is_ray_object = is_wrapped_ray(processor_type)
    if is_ray_object == True:
        processor_type = get_local_processor_type(processor_type)
    processor_keys = get_processor_types()
    p_idx = processor_keys.index(processor_type)
    target_class = __PROC_LIST[p_idx]
    return (
        __wrap_with_ray(target_class, **kwargs)
        if is_ray_object
        else target_class(**kwargs)
    )
