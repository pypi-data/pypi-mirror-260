# Standard imports
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

from typeguard import typechecked


@typechecked
class SamplingMethods(Enum):
    LATIN_HYPERCUBE = "latin_hypercube"
    UNIFORM_RANDOM = "uniform_random"


@typechecked
class Sampling(ABC):
    @abstractmethod
    def to_json(cls, sampling_params: dict):
        pass


@typechecked
class LatinHypercube(Sampling):
    def __init__(
        self, scramble: bool = True, optimization: Optional[str] = "random-cd"
    ):
        self.scramble = scramble
        self.optimization = optimization

    def to_json(self):
        return {
            "method": SamplingMethods.LATIN_HYPERCUBE.value,
            "sampling_params": {
                "scramble": self.scramble,
                "optimization": self.optimization,
            },
        }


@typechecked
class UniformRandom(Sampling):
    def __init__(self):
        pass

    def to_json(self):
        return {
            "method": SamplingMethods.UNIFORM_RANDOM.value,
            "sampling_params": {},
        }
