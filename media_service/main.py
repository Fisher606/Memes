from fastapi import FastAPI, UploadFile, HTTPException
import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError

app = FastAPI()

# Настройки подключения к MinIO
S3_ENDPOINT = "http://127.0.0.1:9000"  # Адрес MinIO
S3_ACCESS_KEY = "minioadmin"  # Логин из терминала MinIO
S3_SECRET_KEY = "minioadmin"  # Пароль из терминала MinIO
BUCKET_NAME = "memes"  # Имя бакета, который ты создал

# Инициализация клиента для работы с MinIO
s3_client = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
)

@app.post("/upload")
async def upload_file(file: UploadFile):
    """
    Загрузить файл в MinIO
    """
    try:
        # Загрузка файла в бакет MinIO
        s3_client.upload_fileobj(
            file.file,
            BUCKET_NAME,
            file.filename,
            ExtraArgs={"ContentType": file.content_type},  # Тип содержимого (например, image/png)
        )
        return {"message": "File uploaded successfully", "filename": file.filename}
    except (BotoCoreError, NoCredentialsError) as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@app.delete("/delete/{filename}")
async def delete_file(filename: str):
    """
    Удалить файл из MinIO
    """
    try:
        # Удаление файла из бакета
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=filename)
        return {"message": "File deleted successfully", "filename": filename}
    except (BotoCoreError, NoCredentialsError) as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")
