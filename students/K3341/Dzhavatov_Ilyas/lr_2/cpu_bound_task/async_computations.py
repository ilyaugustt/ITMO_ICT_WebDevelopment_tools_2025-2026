"""
Задача 1: Вычисление суммы чисел от 1 до N с использованием async.
Каждая асинхронная задача обрабатывает часть диапазона чисел.
"""

import asyncio
import time
from typing import Tuple
from interfaces import Computation


class AsyncComp(Computation):
    async def async_worker(self, start: int, end: int) -> int:
        # Освобождаем event loop для выполнения других задач
        # Но так как это CPU-bound задача, asyncio не ускорит вычисления
        # Из-за GIL в Python, мы используем asyncio для демонстрации синтаксиса
        await asyncio.sleep(0)  # Передача управления другим задачам
        return self.calculate_sum(start, end)

    async def compute(self, num_tasks: int = 4) -> Tuple[float, int]:
        """
        Вычисляет сумму всех чисел от 1 до 1000000000 (10^9)
        с использованием асинхронности.
        """
        total = 10**9
        chunk_size = total // num_tasks

        tasks = []
        for i in range(num_tasks):
            chunk_start = i * chunk_size + 1
            chunk_end = (i + 1) * chunk_size if i < num_tasks - 1 else total
            tasks.append(self.async_worker(chunk_start, chunk_end))

        start_time = time.time()

        results = await asyncio.gather(*tasks)

        elapsed_time = time.time() - start_time

        total_sum = sum(results)

        return elapsed_time, total_sum


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    async_computation = AsyncComp()
    elapsed, result = asyncio.run(async_computation.compute(num_tasks=4))
    logger.info(f"Async результат: {result}")
    logger.info(f"Async время выполнения: {elapsed:.4f} секунд")
