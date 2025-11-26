"""
Оценка качества RAG.
Запуск: python -m app.eval
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from app.rag import retrieve_context, generate_answer, ingest_documents
from app.core.config import settings

TEST_CASES = [
    {
        "question": "Как создать задачу в SmartTask?",
        "must_contain": ["Создание", "задачи", "Нажмите", "+ Задача", "введите", "название"],

    },
    {
        "question": "Что делать, если не отображаются задачи?",
        "must_contain": ["Проверьте", "фильтры", "права", "доступа"]
    },
    {
        "question": "Где взять API-ключ?",
        "must_contain": ["API Guide","получить","настройках", "личный кабинет", "раздел", "ключи", "вашего аккаунта"]
    }
]

def evaluate():
    print("🔍 Запуск eval...")
    passed = 0
    dir_name = os.path.dirname(__file__).replace("app", settings.DOCUMENTS_PATH)
    try:
        ingest_documents(doc_dir=dir_name, force=True)
    except Exception as e:
        print(f"⚠️ Не удалось выполнить импорт документов: {e}")

    for i, case in enumerate(TEST_CASES, 1):
        print(f"\nТест {i}: {case['question']}")
        try:
            context = retrieve_context(case["question"], k=3)
            answer, sources, _, _ = generate_answer(case["question"], context)

            print(f"✅ Ответ: {answer[:100]}...")
            if sources:
                print(f"📄 Источники: {', '.join(sources)}")
            else:
                print("📄 Источники: (пусто) — проверьте, что документы успешно проиндексированы и соответствуют запросу")

            found = any(kw.lower() in answer.lower() for kw in case["must_contain"])
            if found:
                print("🟢 PASS")
                passed += 1
            else:
                print(f"🔴 FAIL (ожидалось одно из: {case['must_contain']})")
        except Exception as e:
            print(f"💥 ERROR: {e}")

    print(f"\n📊 Итог: {passed}/{len(TEST_CASES)}")
    return passed == len(TEST_CASES)

if __name__ == "__main__":
    success = evaluate()
    sys.exit(0 if success else 1)