from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Указываем URL для подключения к SQLite
DATABASE_URL = "sqlite:///./memes.db"

# Создаем объект подключения
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создаем фабрику для сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()
