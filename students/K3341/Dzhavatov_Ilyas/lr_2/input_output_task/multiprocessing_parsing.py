"""
Задача 2: Параллельный парсинг веб-страниц с сохранением в базу данных (multiprocessing).
Каждый процесс загружает и парсит одну или несколько веб-страниц.
"""

import multiprocessing
import time
import psycopg2
from typing import List, Dict, Any, Tuple
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# Список URL для парсинга (2-3 сайта)
URLS = [
    "https://docs.python.org/3/library/asyncio.html",
    "https://docs.python.org/3/library/multiprocessing.html",
    "https://docs.python.org/3/library/threading.html",
]


def fetch_and_parse(url: str) -> Dict[str, Any]:
    """
    Загружает и парсит одну веб-страницу.
    
    Returns:
        словарь с извлеченными данными
    """
    result = {
        "url": url,
        "title": "",
        "meta_description": "",
        "heading_count": 0,
        "link_count": 0,
        "status": 0,
    }
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        response = session.get(url, headers=headers, timeout=30)
        session.close()
        
        result["status"] = response.status_code
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            title_tag = soup.find("title")
            if title_tag:
                result["title"] = title_tag.get_text(strip=True)
            
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if meta_desc:
                result["meta_description"] = meta_desc.get("content", "")
            
            headings = soup.find_all(["h1", "h2", "h3"])
            result["heading_count"] = len(headings)
            
            links = soup.find_all("a", href=True)
            result["link_count"] = len(links)
    except requests.RequestException as e:
        print(f"Ошибка при загрузке {url}: {e}")
    
    return result


def save_to_db(db_config: dict, data: Dict[str, Any]) -> None:
    """Сохраняет данные в PostgreSQL базу данных."""
    try:
        conn = psycopg2.connect(**db_config)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO parsed_pages (url, title, meta_description, heading_count, link_count, status_code)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (url) DO NOTHING
                """,
                (
                    data["url"],
                    data["title"],
                    data["meta_description"],
                    data["heading_count"],
                    data["link_count"],
                    data.get("status", 0),
                ),
            )
        conn.close()
        print(f"Сохранено: {data['title'][:50] if data['title'] else 'N/A'}... ({data['url']})")
    except Exception as e:
        print(f"Ошибка при сохранении {data['url']}: {e}")


def worker(args: Tuple[str, dict]) -> Dict[str, Any]:
    """
    Рабочая функция для multiprocessing.Pool.
    Загружает, парсит и сохраняет данные.
    
    Args:
        args: кортеж (url, db_config)
    """
    url, db_config = args
    result = fetch_and_parse(url)
    
    if result["status"] == 200:
        save_to_db(db_config, result)
    
    return result


def multiprocessing_parse(urls: List[str], num_processes: int = 4) -> Tuple[float, int]:
    """
    Парсит веб-страницы параллельно с использованием multiprocessing.
    
    Args:
        urls: список URL для парсинга
        num_processes: количество процессов
        
    Returns:
        кортеж (время выполнения, количество успешно обработанных страниц)
    """
    db_config = {
        "host": "localhost",
        "database": "lr2_parsing",
        "user": "postgres",
        "password": "postgres"
    }
    
    tasks = [(url, db_config) for url in urls]
    
    start_time = time.time()
    
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(worker, tasks)
    
    elapsed_time = time.time() - start_time
    
    success_count = sum(1 for r in results if r["status"] == 200)
    
    return elapsed_time, success_count


if __name__ == "__main__":
    print("=" * 60)
    print("MULTIPROCESSING: Параллельный парсинг веб-страниц")
    print("=" * 60)
    
    elapsed, count = multiprocessing_parse(URLS, num_processes=4)
    
    print(f"\nРезультаты multiprocessing:")
    print(f"  Обработано страниц: {count}/{len(URLS)}")
    print(f"  Время выполнения: {elapsed:.4f} секунд")
