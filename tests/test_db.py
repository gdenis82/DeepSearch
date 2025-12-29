from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from app.db.session import ASYNC_DATABASE_URL


async def test_db_connection():
    """Проверяет подключение к базе данных через локальный engine."""
    local_engine = create_async_engine(ASYNC_DATABASE_URL)
    try:
        async with local_engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
    finally:
        await local_engine.dispose()