from pms_inference_engine._const import *
from abc import ABCMeta, abstractmethod
import asyncio
from typing import Generic, List
from pms_inference_engine.utility import create_uuid
from pms_inference_engine.interface._i_engine_processor import IEngineProcessor
from pms_inference_engine.data_struct import EngineIOData


class IEngineProcessorPool(Generic[InputTypeT, OutputTypeT], metaclass=ABCMeta):
    def __init__(
        self,
        processors: List[IEngineProcessor[InputTypeT, OutputTypeT]],
        search_delay: float = 0.1,
    ) -> None:
        assert len(processors) > 0
        self._id = create_uuid()
        self._processors = processors
        self._search_delay = search_delay

    def __len__(self):
        return len(self._processors)

    @abstractmethod
    async def _run(
        self,
        target_processor: IEngineProcessor[InputTypeT, OutputTypeT],
        data: EngineIOData,
    ) -> EngineIOData: ...

    async def search_ready(
        self,
    ) -> IEngineProcessor[InputTypeT, OutputTypeT]:
        processors = self._processors
        delay = self.search_delay
        readyed_processors: List[IEngineProcessor[InputTypeT, OutputTypeT]] = []
        while True:
            readyed_processors = list(
                filter(lambda x: x.is_enable_to_run() == True, processors)
            )
            if len(readyed_processors) != 0:
                break
            await asyncio.sleep(delay)
        return readyed_processors[0]

    async def run(
        self,
        data: EngineIOData,
    ) -> EngineIOData:
        target_processor = await self.search_ready()
        result = await self._run(
            target_processor=target_processor,
            data=data,
        )
        return result

    async def __call__(
        self,
        data: EngineIOData,
    ) -> EngineIOData:
        return await self.run(data=data)

    @property
    def id(self) -> str:
        return self._id

    @property
    def search_delay(self) -> float:
        return self._search_delay

    @search_delay.setter
    def search_delay(self, value: float):
        assert value > 0
        self._search_delay = value
