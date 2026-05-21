import uuid
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional
import requests
from bs4 import BeautifulSoup
from celery_config import app as celery_app

app = FastAPI(title="Parser Service", version="1.0.0")


class ParseRequest(BaseModel):
    url: str = Field(..., description="URL веб-страницы для парсинга")
    parse_title: bool = Field(default=True, description="Извлечь заголовок страницы")
    parse_links: bool = Field(default=True, description="Извлечь все ссылки")
    parse_images: bool = Field(default=True, description="Извлечь все изображения")
    parse_meta: bool = Field(default=True, description="Извлечь meta-теги")
    parse_headings: bool = Field(default=True, description="Извлечь заголовки H1-H6")


class ParseResponse(BaseModel):
    url: str
    title: Optional[str] = None
    meta: dict = {}
    headings: list = []
    links: list = []
    images: list = []
    content_length: int = 0
    status_code: int


class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[ParseResponse] = None
    error: Optional[str] = None


@celery_app.task(name="parser.parse_url")
def parse_url_task(url: str, parse_title: bool = True, parse_links: bool = True,
                   parse_images: bool = True, parse_meta: bool = True,
                   parse_headings: bool = True) -> dict:
    """Celery задача для парсинга веб-страницы в фоновом режиме.
    
    Возвращает результат в формате dict для JSON-сериализации.
    """
    try:
        response = requests.get(
            url,
            timeout=30,
            headers={"User-Agent": "Mozilla/5.0 (Parser Service/1.0)"}
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Ошибка при загрузке страницы: {str(e)}")

    soup = BeautifulSoup(response.text, "html.parser")

    result = {
        "url": url,
        "content_length": len(response.text),
        "status_code": response.status_code
    }

    if parse_title:
        title_tag = soup.find("title")
        result["title"] = title_tag.get_text(strip=True) if title_tag else None

    # if parse_meta:
    #     meta_tags = soup.find_all("meta")
    #     for tag in meta_tags:
    #         name = tag.get("name") or tag.get("property") or tag.get("http-equiv")
    #         content = tag.get("content")
    #         if name and content:
    #             result["meta"][name] = content

    if parse_headings:
        headings = []
        for level in range(1, 7):
            for h in soup.find_all(f"h{level}"):
                text = h.get_text(strip=True)
                if text:
                    headings.append({"level": level, "text": text})
        result["headings"] = headings

    if parse_links:
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(strip=True)
            if text:
                links.append({"href": href, "text": text})
        result["links"] = links

    if parse_images:
        images = []
        for img in soup.find_all("img", src=True):
            src = img["src"]
            alt = img.get("alt")
            images.append({"src": src, "alt": alt})
        result["images"] = images

    return result


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/parse", response_model=ParseResponse)
def parse_url_sync(request: ParseRequest):
    """Синхронный парсинг веб-страницы по URL."""
    try:
        response = requests.get(
            request.url,
            timeout=30,
            headers={"User-Agent": "Mozilla/5.0 (Parser Service/1.0)"}
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при загрузке страницы: {str(e)}")

    soup = BeautifulSoup(response.text, "html.parser")

    result = ParseResponse(
        url=request.url,
        content_length=len(response.text),
        status_code=response.status_code
    )

    if request.parse_title:
        title_tag = soup.find("title")
        result.title = title_tag.get_text(strip=True) if title_tag else None

    if request.parse_meta:
        meta_tags = soup.find_all("meta")
        for tag in meta_tags:
            name = tag.get("name") or tag.get("property") or tag.get("http-equiv")
            content = tag.get("content")
            if name and content:
                result.meta[name] = content

    if request.parse_headings:
        headings = []
        for level in range(1, 7):
            for h in soup.find_all(f"h{level}"):
                text = h.get_text(strip=True)
                if text:
                    headings.append({"level": level, "text": text})
        result.headings = headings

    if request.parse_links:
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(strip=True)
            if text:
                links.append({"href": href, "text": text})
        result.links = links

    if request.parse_images:
        images = []
        for img in soup.find_all("img", src=True):
            src = img["src"]
            alt = img.get("alt")
            images.append({"src": src, "alt": alt})
        result.images = images

    return result


@app.post("/parse/async", response_model=TaskResponse)
def parse_url_async(request: ParseRequest):
    """Асинхронный парсинг веб-страницы через Celery очередь.
    
    Возвращает task_id для отслеживания статуса выполнения.
    """
    task = parse_url_task.delay(
        url=request.url,
        parse_title=request.parse_title,
        parse_links=request.parse_links,
        parse_images=request.parse_images,
        parse_meta=request.parse_meta,
        parse_headings=request.parse_headings
    )
    
    return TaskResponse(
        task_id=task.id,
        status="queued",
        message="Задача поставлена в очередь на выполнение"
    )


@app.get("/parse/task/{task_id}", response_model=TaskStatusResponse)
def get_task_status(task_id: str):
    from celery.result import AsyncResult
    
    task = AsyncResult(task_id, app=celery_app)
    
    if task.state == "PENDING":
        return TaskStatusResponse(
            task_id=task_id,
            status="pending",
            error="Задача ожидает выполнения"
        )
    elif task.state == "STARTED":
        return TaskStatusResponse(
            task_id=task_id,
            status="started",
            error="Задача выполняется"
        )
    elif task.state == "SUCCESS":
        result = task.get(timeout=10)
        return TaskStatusResponse(
            task_id=task_id,
            status="completed",
            result=result
        )
    elif task.state == "FAILURE":
        return TaskStatusResponse(
            task_id=task_id,
            status="failed",
            error=str(task.result)
        )
    else:
        return TaskStatusResponse(
            task_id=task_id,
            status=task.state.lower(),
            error="Задача в неизвестном состоянии"
        )


@app.get("/parse/simple")
def parse_url_simple(url: str = Query(..., description="URL веб-страницы для парсинга")):
    """Простой endpoint для синхронного парсинга без тела запроса."""
    request = ParseRequest(url=url)
    return parse_url_sync(request)
