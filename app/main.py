from fastapi import FastAPI, HTTPException, UploadFile, Form
from fastapi.responses import JSONResponse
import httpx
from pydantic import BaseModel

app = FastAPI()

# URL второго сервиса (media_service)
MEDIA_SERVICE_URL = "http://127.0.0.1:8001"

# Модель для мемов
class Meme(BaseModel):
    id: int
    text: str
    image_url: str


# Временное хранилище для мемов (имитация базы данных)
memes = {}
next_id = 1


@app.get("/memes")
async def get_memes():
    """
    Получить список всех мемов
    """
    return list(memes.values())


@app.get("/memes/{id}")
async def get_meme(id: int):
    """
    Получить конкретный мем по ID
    """
    meme = memes.get(id)
    if not meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    return meme


@app.post("/memes")
async def create_meme(text: str = Form(...), image: UploadFile = None):
    """
    Создать новый мем
    """
    global next_id

    # Загружаем файл в MinIO через media_service
    if image:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{MEDIA_SERVICE_URL}/upload", files={"file": (image.filename, image.file, image.content_type)}
            )
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to upload image")
            image_url = f"{MEDIA_SERVICE_URL}/files/{image.filename}"
    else:
        image_url = None

    # Создаём новый мем
    new_meme = Meme(id=next_id, text=text, image_url=image_url)
    memes[next_id] = new_meme
    next_id += 1

    return new_meme


@app.put("/memes/{id}")
async def update_meme(id: int, text: str = Form(None), image: UploadFile = None):
    """
    Обновить существующий мем
    """
    meme = memes.get(id)
    if not meme:
        raise HTTPException(status_code=404, detail="Meme not found")

    # Обновляем текст, если он указан
    if text:
        meme.text = text

    # Если передано новое изображение, загружаем его
    if image:
        # Удаляем старое изображение, если оно есть
        if meme.image_url:
            filename = meme.image_url.split("/")[-1]
            async with httpx.AsyncClient() as client:
                await client.delete(f"{MEDIA_SERVICE_URL}/delete/{filename}")

        # Загружаем новое изображение
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{MEDIA_SERVICE_URL}/upload", files={"file": (image.filename, image.file, image.content_type)}
            )
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to upload image")
            meme.image_url = f"{MEDIA_SERVICE_URL}/files/{image.filename}"

    memes[id] = meme
    return meme


@app.delete("/memes/{id}")
async def delete_meme(id: int):
    """
    Удалить мем
    """
    meme = memes.pop(id, None)
    if not meme:
        raise HTTPException(status_code=404, detail="Meme not found")

    # Удаляем изображение из MinIO, если оно есть
    if meme.image_url:
        filename = meme.image_url.split("/")[-1]
        async with httpx.AsyncClient() as client:
            await client.delete(f"{MEDIA_SERVICE_URL}/delete/{filename}")

    return JSONResponse(content={"message": "Meme deleted successfully"})
