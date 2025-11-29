from app.cache import hash_query, get_cache, set_cache, redis_client


async def test_cache_integration():
    question = "Test question for integration"
    cache_key = await hash_query(question)

    # удаляем ключ перед началом теста, чтобы гарантировать чистое состояние
    await redis_client.delete(cache_key)

    try:
        # Проверяем, что кэша нет
        assert await get_cache(cache_key) is None

        # Записываем в кэш
        result = {"answer": "Test answer", "source": "integration_test"}
        await set_cache(cache_key, result, ttl=60)

        # Читаем и проверяем
        retrieved = await get_cache(cache_key)
        assert retrieved == result

        # Дополнительно: проверим, что Redis хранит именно JSON-строку
        raw_value = await redis_client.get(cache_key)
        assert raw_value is not None
        assert '"answer": "Test answer"' in raw_value

    finally:
        # Чистим за собой
        deleted_count = await redis_client.delete(cache_key)
        print(f"Cleaned up test key '{cache_key}' (deleted: {deleted_count})")