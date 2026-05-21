#!/usr/bin/env python3
"""
Основная программа для сравнения подходов threading, multiprocessing и async.
Задача 2: Парсинг веб-страниц с сохранением в PostgreSQL.
"""

import time
import asyncio
from typing import Dict, List, Tuple

from threading_parsing import threading_parse
from multiprocessing_parsing import multiprocessing_parse
from async_parsing import async_parse


# Список URL для парсинга (2-3 сайта)
URLS = [
    "https://docs.python.org/3/library/asyncio.html",
    "https://docs.python.org/3/library/multiprocessing.html",
    "https://docs.python.org/3/library/threading.html",
]


def run_comparison():
    """Запускает сравнение всех подходов."""
    num_workers = 4

    results: Dict[str, Dict[str, float]] = {}

    print("=" * 70)
    print("СРАВНЕНИЕ ПОДХОДОВ: Threading vs Multiprocessing vs Async")
    print("=" * 70)
    print(f"Задача: Парсинг {len(URLS)} веб-страниц с сохранением в PostgreSQL")
    print(f"URLs: {URLS}")
    print("=" * 70)
    print()

    # 1. Threading
    print("[1/3] Запуск threading (4 потока)...")
    elapsed, count = threading_parse(URLS, num_threads=num_workers)
    results["Threading"] = {"time": elapsed, "count": count}
    print(f"  Threading: {elapsed:.4f} сек | Обработано: {count}/{len(URLS)}")
    print()

    # 2. Multiprocessing
    print("[2/3] Запуск multiprocessing (4 процесса)...")
    elapsed, count = multiprocessing_parse(URLS, num_processes=num_workers)
    results["Multiprocessing"] = {"time": elapsed, "count": count}
    print(f"  Multiprocessing: {elapsed:.4f} сек | Обработано: {count}/{len(URLS)}")
    print()

    # 3. Async
    print("[3/3] Запуск async (4 задачи)...")
    elapsed, count = asyncio.run(async_parse(URLS, num_tasks=num_workers))
    results["Async"] = {"time": elapsed, "count": count}
    print(f"  Async: {elapsed:.4f} сек | Обработано: {count}/{len(URLS)}")
    print()

    # =============================================================================
    # Таблица результатов
    # =============================================================================

    print("=" * 70)
    print("РЕЗУЛЬТАТЫ СРАВНЕНИЯ")
    print("=" * 70)
    print()

    header = f"{'Подход':<20} {'Время (сек)':<15} {'Обработано':<15}"
    separator = "-" * len(header)
    print(separator)
    print(header)
    print(separator)

    for approach, data in results.items():
        print(f"{approach:<20} {data['time']:<15.4f} {int(data['count']):<15}")

    print(separator)
    print()

    # =============================================================================
    # Анализ результатов
    # =============================================================================

    print("=" * 70)
    print("АНАЛИЗ РЕЗУЛЬТАТОВ")
    print("=" * 70)
    print()

    print("1. Threading (threading):")
    print(f"   - Время: {results['Threading']['time']:.4f} сек")
    print()

    print("2. Multiprocessing (multiprocessing):")
    print(f"   - Время: {results['Multiprocessing']['time']:.4f} сек")
    print()

    print("3. Async (asyncio):")
    print(f"   - Время: {results['Async']['time']:.4f} сек")
    print()

    fastest = min(results, key=lambda x: results[x]["time"])

    print("=" * 70)
    print(f"Самый быстрый подход: {fastest}")
    print("=" * 70)


if __name__ == "__main__":
    run_comparison()
