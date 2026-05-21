"""
Задача 2: Параллельный парсинг веб-страниц с сохранением в базу данных (async).
Каждая асинхронная задача загружает и парсит одну или несколько веб-страниц.
"""

import asyncio
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Tuple
from bs4 import BeautifulSoup
import aiohttp


URLS = [
    "https://docs.python.org/3/library/asyncio.html",
    "https://docs.python.org/3/library/multiprocessing.html",
    "https://docs.python.org/3/library/threading.html",
]


def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="lr2_parsing",
        user="postgres",
        password="postgres"
    )
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS parsed_pages (
                id SERIAL PRIMARY KEY,
                url TEXT NOT NULL UNIQUE,
                title TEXT,
                meta_description TEXT,
                heading_count INTEGER DEFAULT 0,
                link_count INTEGER DEFAULT 0,
                status_code INTEGER,
                parsed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    return conn


def parse_html(html_content: str, url: str) -> Dict[str, Any]:
    result = {
        "url": url,
        "title": "",
        "meta_description": "",
        "heading_count": 0,
        "link_count": 0,
        "status": 0,
    }
    
    if not html_content:
        return result
    
    soup = BeautifulSoup(html_content, "html.parser")
    
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
    
    return result


def save_to_db(conn, data: Dict[str, Any]) -> None:
    try:
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
                    data["status"],
                ),
            )
        print(f"Сохранено: {data['title'][:50] if data['title'] else 'N/A'}... ({data['url']})")
    except Exception as e:
        print(f"Ошибка при сохранении {data['url']}: {e}")


async def parse_and_save_async(url: str, session: aiohttp.ClientSession, conn) -> Dict[str, Any]:
    result = {
        "url": url,
        "title": "",
        "meta_description": "",
        "heading_count": 0,
        "link_count": 0,
        "status": 0,
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as response:
            result["status"] = response.status
            
            if response.status == 200:
                html_content = await response.text()
                result.update(parse_html(html_content, url))
                save_to_db(conn, result)
            else:
                print(f"Пропущено (статус {response.status}): {url}")
    except asyncio.TimeoutError:
        print(f"Таймаут при загрузке {url}")
    except aiohttp.ClientError as e:
        print(f"Ошибка при загрузке {url}: {e}")
    
    return result


async def async_parse(urls: List[str], num_tasks: int = 4) -> Tuple[float, int]:
    """
    Парсит веб-страницы асинхронно.
    
    Args:
        urls: список URL для парсинга
        num_tasks: количество одновременных задач
        
    Returns:
        кортеж (время выполнения, количество успешно обработанных страниц)
    """
    conn = get_db_connection()
    
    connector = aiohttp.TCPConnector(limit=num_tasks, force_close=True)
    timeout = aiohttp.ClientTimeout(total=30)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = []
        for url in urls:
            task = parse_and_save_async(url, session, conn)
            tasks.append(task)
        
        start_time = time.time()
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        elapsed_time = time.time() - start_time
    
    success_count = sum(1 for r in results if isinstance(r, dict) and r["status"] == 200)
    
    conn.close()
    
    return elapsed_time, success_count


if __name__ == "__main__":
    print("=" * 60)
    print("ASYNC: Параллельный парсинг веб-страниц")
    print("=" * 60)
    
    elapsed, count = asyncio.run(async_parse(URLS, num_tasks=4))
    
    print(f"\nРезультаты async:")
    print(f"  Обработано страниц: {count}/{len(URLS)}")
    print(f"  Время выполнения: {elapsed:.4f} секунд")
