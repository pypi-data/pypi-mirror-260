import asyncio
from pms_inference_engine.interface import IEngineProcessor
from pms_inference_engine.data_struct import EngineIOData
from pms_inference_engine._processor_factory import register


@register
class SleepAndPassProcessor(IEngineProcessor[EngineIOData, EngineIOData]):
    def __init__(
        self,
        concurrency: int,
        index: int,
        sleep_time: float = 0.1,
    ) -> None:
        super().__init__(
            concurrency=concurrency,
            index=index,
        )
        self._sleep_time = sleep_time

    async def _run(self, input_data: EngineIOData) -> EngineIOData:
        await asyncio.sleep(self._sleep_time)
        return input_data

    def _ready_processor(self) -> bool:
        return True

    def _bind_io(self, input_data: EngineIOData):
        return True

    def _get_live(self) -> bool:
        return True

    def _get_concurrency(self) -> int:
        return self._concurrency
