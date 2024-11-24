# Мем-проект

## Описание проекта

Проект представляет собой веб-приложение, которое предоставляет API для работы с коллекцией мемов. Система состоит из нескольких сервисов: публичного API на FastAPI для работы с мемами и медиа-сервиса для работы с изображениями, использующего MinIO для хранения медиа-файлов.

## Стек технологий

- Python
- FastAPI
- PostgreSQL
- MinIO
- Docker
- Docker Compose

## Шаги для запуска

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/username/memes_project.git
    cd memes_project
    ```

2. Запустите проект с помощью Docker Compose:

    ```bash
    docker-compose up --build
    ```

3. После того как контейнеры запустятся, доступ к API будет по адресу:

    - Публичный API: http://127.0.0.1:8000
    - Swagger UI: http://127.0.0.1:8000/docs
    - MinIO Console: http://127.0.0.1:9001

## Описание Docker Compose

- `app`: Основной сервис API на FastAPI.
- `media_service`: Сервис для загрузки и работы с медиа-файлами (MinIO).
- `db`: PostgreSQL для хранения данных.
- `minio`: Хранилище для изображений.
- `minio_console`: Веб-интерфейс для управления MinIO.

## Пример запросов

- **Получить список мемов**:  
  Получить все мемы с пагинацией.

    ```bash
    curl -X 'GET' \
      'http://127.0.0.1:8000/memes?page=1&size=10' \
      -H 'accept: application/json'
    ```

- **Добавить новый мем**:  
  Добавить новый мем с изображением и текстом.

    ```bash
    curl -X 'POST' \
      'http://127.0.0.1:8000/memes' \
      -H 'accept: application/json' \
      -H 'Content-Type: multipart/form-data' \
      -F 'file=@"/path/to/meme_image.jpg"' \
      -F 'text="Funny meme text"'
    ```

## Тестирование

Для тестирования API можно использовать Postman или Swagger UI. Также в проекте написаны unit-тесты, которые можно запустить с помощью:

```bash
pytest 
```










