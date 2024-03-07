from pms_inference_engine._const import *
from abc import ABCMeta, abstractmethod
from typing import Generic
from pms_inference_engine.utility import create_uuid


class IEngineProcessor(Generic[InputTypeT, OutputTypeT], metaclass=ABCMeta):
    def __init__(
        self,
        index: int,
        concurrency: int,
    ) -> None:
        self.__id = create_uuid()
        self._concurrency = concurrency
        self._index = index
        self.__current_concurrency = 0
        self.__ready = self._ready_processor()
        self.__is_io_binded = False

    @abstractmethod
    def _ready_processor(self) -> bool: ...

    @abstractmethod
    def _bind_io(self, input_data: InputTypeT) -> bool: ...

    @abstractmethod
    def _get_live(self) -> bool: ...

    @abstractmethod
    def _get_concurrency(self) -> int: ...

    @abstractmethod
    async def _run(self, input_data: InputTypeT) -> OutputTypeT: ...

    async def run(self, input_data: InputTypeT) -> OutputTypeT:
        if not self.is_io_binded:
            self.__is_io_binded = self._bind_io(input_data=input_data)
        assert self.is_io_binded, "The Processor's IO has not been binded."
        assert self.live, "The Processor is not alive."
        assert self.ready, "The Processor is not ready."
        self.__current_concurrency += 1
        result = await self._run(input_data)
        self.__current_concurrency -= 1
        return result

    async def __call__(self, input_data: InputTypeT) -> OutputTypeT:
        return await self.run(input_data=input_data)

    def is_enable_to_run(
        self,
    ) -> bool:  # ray processor에서 사용됩니다. property로 변경할 수 없습니다.
        __val = self.ready and (self.current_concurrency < self.concurrency)
        return __val

    @property
    def id(self) -> str:
        assert self.__id is not None
        return self.__id

    @property
    def live(self) -> bool:
        __val = self._get_live()
        assert type(__val) is bool
        return __val

    @property
    def ready(self) -> bool:
        return self.__ready

    @property
    def concurrency(self) -> int:
        __val = self._get_concurrency()
        assert type(__val) is int
        assert __val > 0
        return __val

    @property
    def current_concurrency(self) -> int:
        __val = self.__current_concurrency
        return __val

    @property
    def is_io_binded(self) -> bool:
        return self.__is_io_binded
