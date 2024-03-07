from pms_inference_engine._const import *
from typing import List
from pms_inference_engine.data_struct import EngineIOData
from pms_inference_engine.interface import IEngineProcessor, IEngineProcessorPool
import time


class ProcessorPool(IEngineProcessorPool[EngineIOData, EngineIOData]):
    def __init__(
        self,
        processors: List[IEngineProcessor],
        search_delay: float = 0.1,
    ) -> None:
        super().__init__(processors, search_delay)

    async def _run(
        self,
        target_processor: IEngineProcessor,
        data: EngineIOData,
    ) -> EngineIOData:
        assert data is not None, "The data is None"
        assert type(data) is EngineIOData, "The data is wrong type"
        LOGGER.debug(
            f"processor[{self._processors.index(target_processor)}] process start"
        )
        start = time.time()
        result = await target_processor(data)
        end = time.time()
        LOGGER.debug(
            f"processor[{self._processors.index(target_processor)}] process complete | frame={data.frame_id:08d} | time={end-start:.4f} sec"
        )
        assert result is not None, "The result is None"
        assert type(result) is EngineIOData, "The result is wrong type"
        return result

    def __len__(self):
        processors: List[IEngineProcessor] = self._processors
        return sum([p.concurrency for p in processors])
