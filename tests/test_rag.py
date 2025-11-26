from app.rag import retrieve_context

async def test_retrieve_context():
    # Должен вернуть хотя бы 1 результат
    results = await retrieve_context("Что такое SmartTask?", k=1)
    assert isinstance(results, list)
    assert len(results) >= 1
    assert "text" in results[0]
    assert "source" in results[0]
    assert isinstance(results[0]["text"], str)
    assert ".pdf" in results[0]["source"]