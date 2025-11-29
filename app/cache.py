import logging

import redis.asyncio as aioredis
import json
import hashlib
from typing import Optional, Dict, Any

from app.core.config import settings

logger = logging.getLogger(__name__)


class _RedisFacade:
    """Упрощенный интерфейс, который создает новый клиент Redis asyncio для каждого вызова.

    Обоснование:
    Сохранение одного соединения Redis в разных циклах может привести к
    ошибкам "Будущее подключено к другому циклу". Создавая кратковременный
    для каждой операции мы гарантируем, что соединение привязано к текущему
    циклу и затем немедленно закрывается.
    """

    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port

    def _client(self) -> aioredis.Redis:
        return aioredis.Redis(
            host=self._host,
            port=self._port,
            decode_responses=True,
            socket_connect_timeout=2,
            socket_timeout=2,
        )

    async def get(self, key: str):
        client = self._client()
        try:
            return await client.get(key)
        finally:
            # ensure underlying connections are closed to avoid loop leakage
            await client.aclose()

    async def setex(self, key: str, ttl: int, value: str):
        client = self._client()
        try:
            return await client.setex(key, ttl, value)
        finally:
            await client.aclose()

    async def delete(self, *keys: str):
        client = self._client()
        try:
            return await client.delete(*keys)
        finally:
            await client.aclose()


redis_client = _RedisFacade(settings.REDIS_HOST, int(settings.REDIS_PORT))


async def hash_query(query: str) -> str:
    return hashlib.md5(query.lower().strip().encode("utf-8")).hexdigest()


async def get_cache(key: str) -> Optional[Dict[str, Any]]:
    try:
        cached = await redis_client.get(key)
        return json.loads(cached) if cached else None
    except Exception as e:
        logger.error(f"Redis get failed: {e}")
        return None


async def set_cache(key: str, value: Dict[str, Any], ttl: int = 3600):
    try:
        await redis_client.setex(key, ttl, json.dumps(value, ensure_ascii=False))
    except Exception as e:
        logger.error(f"Redis set failed: {e}")
