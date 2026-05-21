"""
Задача 1: Вычисление суммы чисел от 1 до N с использованием threading.
Каждая нить обрабатывает часть диапазона чисел.
"""

import threading
import time
from typing import List, Tuple

from interfaces import Computation


class ThreadComp(Computation):
    def compute(self, num_tasks: int) -> Tuple[float, int]:
        """
        Вычисляет сумму всех чисел от 1 до 1000000000 (10^9)
        с использованием многопоточности.
        """
        num_threads = num_tasks
        total = 10**9
        chunk_size = total // num_threads

        threads: List[threading.Thread] = []
        results: List[int] = [0] * num_threads
        results_index = [0]  # Используем список для мутации во вложенной функции

        start_time = time.time()

        def thread_worker(thread_index: int, chunk_start: int, chunk_end: int):
            results[thread_index] = self.calculate_sum(chunk_start, chunk_end)

        for i in range(num_threads):
            chunk_start = i * chunk_size + 1
            chunk_end = (i + 1) * chunk_size if i < num_threads - 1 else total
            thread = threading.Thread(
                target=thread_worker, args=(i, chunk_start, chunk_end)
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        elapsed_time = time.time() - start_time

        total_sum = sum(results)

        return elapsed_time, total_sum


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    thread_comp = ThreadComp()
    elapsed, result = thread_comp.compute(num_tasks=4)
    logger.info(f"Threading результат: {result}")
    logger.info(f"Threading время выполнения: {elapsed:.4f} секунд")
