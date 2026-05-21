
import threading
import time
import psycopg2
from typing import List, Dict, Any, Tuple
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


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


def fetch_page(url: str, session: requests.Session) -> Tuple[str, int]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        response = session.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text, response.status_code
    except requests.RequestException as e:
        print(f"Ошибка при загрузке {url}: {e}")
        return "", 0


def parse_html(html_content: str, url: str) -> Dict[str, Any]:
    """
    Парсит HTML-содержимое и извлекает информацию.
    
    Returns:
        словарь с извлеченными данными
    """
    result = {
        "url": url,
        "title": "",
        "meta_description": "",
        "heading_count": 0,
        "link_count": 0,
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
    """Сохраняет данные в PostgreSQL базу данных."""
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
                    data.get("status", 0),
                ),
            )
        print(f"Сохранено: {data['title'][:50] if data['title'] else 'N/A'}... ({data['url']})")
    except Exception as e:
        print(f"Ошибка при сохранении {data['url']}: {e}")


def parse_and_save_threading(url: str, session: requests.Session, conn) -> None:
    html, status = fetch_page(url, session)
    if status == 200:
        data = parse_html(html, url)
        save_to_db(conn, data)
    else:
        print(f"Пропущено (статус {status}): {url}")


def threading_parse(urls: List[str], num_threads: int = 4) -> Tuple[float, int]:
    conn = get_db_connection()
    
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    threads: List[threading.Thread] = []
    success_count = [0]
    
    start_time = time.time()
    
    def thread_worker(url: str):
        try:
            parse_and_save_threading(url, session, conn)
            success_count[0] += 1
        except Exception as e:
            print(f"Ошибка в потоке для {url}: {e}")
    
    for url in urls:
        thread = threading.Thread(target=thread_worker, args=(url,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    elapsed_time = time.time() - start_time
    
    session.close()
    conn.close()
    
    return elapsed_time, success_count[0]


if __name__ == "__main__":
    print("=" * 60)
    print("THREADING: Параллельный парсинг веб-страниц")
    print("=" * 60)
    
    elapsed, count = threading_parse(URLS, num_threads=4)
    
    print(f"\nРезультаты threading:")
    print(f"  Обработано страниц: {count}/{len(URLS)}")
    print(f"  Время выполнения: {elapsed:.4f} секунд")
