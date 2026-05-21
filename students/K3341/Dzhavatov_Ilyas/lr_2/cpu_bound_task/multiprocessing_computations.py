"""
Задача 1: Вычисление суммы чисел от 1 до N с использованием multiprocessing.
Каждый процесс обрабатывает часть диапазона чисел.
"""

import multiprocessing
import time
from typing import Tuple
from interfaces import Computation


class MultiProc(Computation):
    def compute(self, num_tasks: int) -> Tuple[float, int]:
        num_processes = num_tasks
        total = 10**9
        chunk_size = total // num_processes

        tasks = []
        for i in range(num_processes):
            chunk_start = i * chunk_size + 1
            chunk_end = (i + 1) * chunk_size if i < num_processes - 1 else total
            tasks.append((chunk_start, chunk_end))

        start_time = time.time()

        with multiprocessing.Pool(processes=num_processes) as pool:
            results = pool.map(self.worker, tasks)

        elapsed_time = time.time() - start_time

        total_sum = sum(results)

        return elapsed_time, total_sum

    def worker(self, args: Tuple[int, int]) -> int:
        start, end = args
        return self.calculate_sum(start, end)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    multi_proc = MultiProc()
    elapsed, result = multi_proc.compute(num_tasks=4)
    logger.info(f"Multiprocessing результат: {result}")
    logger.info(f"Multiprocessing время выполнения: {elapsed:.4f} секунд")
