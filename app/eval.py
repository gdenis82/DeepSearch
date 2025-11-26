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
        "sources" : ["SmartTask_User_Manual.pdf"]
    },
    {
        "question": "Что делать, если не отображаются задачи?",
        "must_contain": ["Проверьте", "фильтры", "права", "доступа"],
        "sources" : ["SmartTask_Troubleshooting_Guide.pdf"]
    },
    {
        "question": "Где взять API-ключ?",
        "must_contain": ["API Guide","получить","настройках", "личный кабинет", "раздел", "ключи", "вашего аккаунта"],
        "sources" : ["SmartTask_API_Guide.pdf"]
    }
]

def evaluate():
    print("🔍 Запуск eval...")
    passed = 0


    for i, case in enumerate(TEST_CASES, 1):
        print(f"\nТест {i}: {case['question']}")
        try:
            context = retrieve_context(case["question"], k=3)
            answer, sources, _, _ = generate_answer(case["question"], context)

            print(f"✅ Ответ: {answer[:100]}...")
            if sources:
                print(f"📄 Источники: {', '.join(sources)}")

            found = any(kw.lower() in answer.lower() for kw in case["must_contain"])
            found_sources =  any(kw in sources for kw in case["sources"])
            if found and found_sources:
                print("🟢 PASS")
                passed += 1
            else:
                print(f"🔴 FAIL (ожидалось одно из: {case['must_contain']} и источники {case['sources']})")
        except Exception as e:
            print(f"💥 ERROR: {e}")

    print(f"\n📊 Итог: {passed}/{len(TEST_CASES)}")
    return passed == len(TEST_CASES)

if __name__ == "__main__":
    success = evaluate()
    sys.exit(0 if success else 1)