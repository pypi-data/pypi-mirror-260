from pms_inference_engine._const import *
from pms_inference_engine.interface import IEngineProcessor
import ray
from typing import Type
from pms_inference_engine.utility import get_local_placement_strategy


class RayProcessor(IEngineProcessor[InputTypeT, OutputTypeT]):

    def __init__(
        self,
        target_class: Type[IEngineProcessor],
        concurrency: int,
        index: int,
        **kwargs,
    ) -> None:
        self._concurrency = concurrency
        self._target_class = target_class
        self._index = index
        self._kwargs = kwargs
        super().__init__(
            concurrency=concurrency,
            index=index,
        )
        assert issubclass(target_class, IEngineProcessor)

    async def _run(self, input_data: InputTypeT) -> OutputTypeT:
        r = await self._remote_processor.run.remote(input_data=input_data)
        return r

    def _ready_processor(self) -> bool:
        concurrency = self._concurrency
        target_class = self._target_class
        index = self._index
        kwargs = self._kwargs
        actor_options = {
            "max_concurrency": concurrency,
            "scheduling_strategy": get_local_placement_strategy(),
        }
        self._remote_processor = (
            ray.remote(target_class)
            .options(**actor_options)  # type: ignore
            .remote(
                concurrency=concurrency,
                index=index,
                **kwargs,
            )
        )
        return self._remote_processor.is_enable_to_run.remote()

    def _bind_io(self, input_data: InputTypeT):
        return True

    def _get_live(self) -> bool:
        ray_obj_ref: ray.ObjectRef = self._remote_processor._get_live.remote()
        __val = ray.get(ray_obj_ref)
        return __val

    def _get_concurrency(self) -> int:
        return self._concurrency
