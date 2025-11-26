import os
from typing import List, Optional
import logging

from dotenv import load_dotenv, find_dotenv
from pydantic import AnyHttpUrl, PostgresDsn
from pydantic_settings import BaseSettings

logger = logging.getLogger("faq")
load_dotenv(find_dotenv())

class Settings(BaseSettings):
    ENVIRONMENT: str
    PROJECT_NAME: str = "SmartTask FAQ"
    API_V1_STR: str = "/api/v1"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", '')
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", '')
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

    ANSWER_PROMPT: str = os.getenv(
        "ANSWER_PROMPT",
        """Вы — эксперт по продукту SmartTask. Отвечайте чётко и по делу. 
        Используйте ТОЛЬКО информацию из приведённого контекста. 
        Если в контексте нет ответа — напишите: «Извините, я не знаю ответа на этот вопрос».""")

    # Security settings
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str

    # CORS settings
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:8000",
                                              "http://127.0.0.1:8000", ]
    # Path to ChromaDB
    CHROMA_PATH: str = os.getenv('CHROMA_PATH', './data/chroma_db')

    # Path to documents
    DOCUMENTS_PATH: str = os.getenv('DOCUMENTS_PATH', './data/documents')

    # Redis
    REDIS_HOST: str = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT: int = os.getenv('REDIS_PORT', 6379)

    # Postgres
    POSTGRES_HOST: str = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_USER: str = os.getenv('POSTGRES_USER', 'faquser')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', 'faqpass')
    POSTGRES_DB: str = os.getenv('POSTGRES_DB', 'faqdb')
    POSTGRES_PORT: int = os.getenv('POSTGRES_PORT', 5432)
    DATABASE_URL: Optional[PostgresDsn] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # If in development and a local DB URL is provided, prefer it
        if (self.ENVIRONMENT or '').lower() == 'development':
            logger.info("Using development (backend running locally)")
            self.POSTGRES_HOST = 'localhost'
            self.REDIS_HOST = 'localhost'

        self.DATABASE_URL = (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )



# Initialize settings with logging
try:
    # Use a local logger here to avoid importing app.utils and creating a circular import

    settings = Settings()
    logger.info("Settings loaded successfully")
except Exception as e:
    logger.error(f"Error loading settings: {e}")
    raise