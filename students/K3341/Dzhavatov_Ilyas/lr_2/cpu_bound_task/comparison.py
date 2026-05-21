#!/usr/bin/env python3
"""
Основная программа для сравнения подходов threading, multiprocessing и async.
Задача 1: Вычисление суммы всех чисел от 1 до N.
Использует реализованные классы из модулей.
"""

import asyncio
from typing import Dict

from interfaces import Computation
from threading_computations import ThreadComp
from multiprocessing_computations import MultiProc
from async_computations import AsyncComp


def run_comparison():
    """Запускает сравнение всех подходов."""
    num_tasks = 4

    results: Dict[str, Dict[str, float]] = {}

    print("=" * 70)
    print("СРАВНЕНИЕ ПОДХОДОВ: Threading vs Multiprocessing vs Async")
    print("=" * 70)
    print(f"Задача: Вычислить сумму чисел от 1 до 10^9 ({10**9:,})")
    print(f"Ожидаемый результат: {10**9 * (10**9 + 1) // 2:,}")
    print("=" * 70)
    print()

    # 1. Threading
    print(f"[1/3] Запуск threading ({num_tasks} потока)...")
    thread_comp = ThreadComp()
    elapsed, result = thread_comp.compute(num_tasks)
    results["Threading"] = {"time": elapsed, "result": result}
    print(f"  Threading: {elapsed:.4f} сек | Результат: {result:,}")
    print()

    # 2. Multiprocessing
    print(f"[2/3] Запуск multiprocessing ({num_tasks} процесса)...")
    multi_proc = MultiProc()
    elapsed, result = multi_proc.compute(num_tasks)
    results["Multiprocessing"] = {"time": elapsed, "result": result}
    print(f"  Multiprocessing: {elapsed:.4f} сек | Результат: {result:,}")
    print()

    # 3. Async
    print(f"[3/3] Запуск async ({num_tasks} задачи)...")
    async_comp = AsyncComp()
    elapsed, result = asyncio.run(async_comp.compute(num_tasks))
    results["Async"] = {"time": elapsed, "result": result}
    print(f"  Async: {elapsed:.4f} сек | Результат: {result:,}")
    print()

    # =============================================================================
    # Таблица результатов
    # =============================================================================

    print("=" * 70)
    print("РЕЗУЛЬТАТЫ СРАВНЕНИЯ")
    print("=" * 70)
    print()

    header = f"{'Подход':<20} {'Время (сек)':<15} {'Результат':<20}"
    separator = "-" * len(header)
    print(separator)
    print(header)
    print(separator)

    for approach, data in results.items():
        print(f"{approach:<20} {data['time']:<15.4f} {data['result']:<20,}")

    print(separator)
    print()

    # =============================================================================
    # Анализ результатов
    # =============================================================================

    print("=" * 70)
    print("АНАЛИЗ РЕЗУЛЬТАТОВ")
    print("=" * 70)
    print()

    # Находим самый быстрый подход
    fastest = min(results, key=lambda x: results[x]["time"])

    print("1. Threading (threading):")
    print("   - Использует GIL (Global Interpreter Lock) в Python")
    print("   - Подходит для I/O-bound задач (сеть, файлы)")
    print("   - Для CPU-bound задач (вычисления) не даёт ускорения из-за GIL")
    print(f"   - Время: {results['Threading']['time']:.4f} сек")
    print()

    print("2. Multiprocessing (multiprocessing):")
    print("   - Обходит GIL, создавая отдельные процессы с собственной памятью")
    print("   - Идеально для CPU-bound задач")
    print("   - Наивысшее ускорение для вычислений")
    print("   - Накладные расходы на создание процессов и межпроцессное взаимодействие")
    print(f"   - Время: {results['Multiprocessing']['time']:.4f} сек")
    print()

    print("3. Async (asyncio):")
    print("   - Однопоточный, использует event loop")
    print("   - Идеально для I/O-bound задач (сеть, файлы)")
    print("   - Для CPU-bound задач не даёт ускорения (тот же поток)")
    print("   - Минимальные накладные расходы на переключение задач")
    print(f"   - Время: {results['Async']['time']:.4f} сек")
    print()

    print("=" * 70)
    print(f"Самый быстрый параллельный подход: {fastest}")
    print("=" * 70)


if __name__ == "__main__":
    run_comparison()
