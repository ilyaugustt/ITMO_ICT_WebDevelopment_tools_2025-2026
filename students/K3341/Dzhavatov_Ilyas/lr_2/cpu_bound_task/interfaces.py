from abc import ABC, abstractmethod
from typing import Tuple


class Computation(ABC):
    @abstractmethod
    def compute(self, num_tasks: int) -> Tuple[float, int]: ...

    @abstractmethod
    async def compute(self, num_tasks: int) -> Tuple[float, int]: ...

    def calculate_sum(self, start: int, end: int) -> int:
        return sum(range(start, end + 1))
