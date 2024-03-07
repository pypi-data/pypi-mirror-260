from typing import TypeVar
import loguru

# logger
LOGGER = loguru.logger

# type def
InputTypeT = TypeVar("InputTypeT")
OutputTypeT = TypeVar("OutputTypeT")
ProcessorTypeT = TypeVar("ProcessorTypeT")

# processor prefix
RAY_PROCESSOR_PREFIX = "Ray_"
