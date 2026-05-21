from abc import ABC, abstractmethod
from typing import List, Tuple


class Parsing(ABC):
    @abstractmethod
    def parse(self, urls: List[str], num_workers: int) -> Tuple[float, int]: ...

    @abstractmethod
    async def parse(self, urls: List[str], num_workers: int) -> Tuple[float, int]: ...

    def get_db_config(self) -> dict:
        return {
            "host": "localhost",
            "database": "lr2_parsing",
            "user": "postgres",
            "password": "postgres"
        }
