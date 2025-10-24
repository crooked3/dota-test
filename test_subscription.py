import asyncio
import httpx

async def test():
    # Тест проверки подписки
    url = "http://localhost:5000/check-subscription"
    
    # Создаём тестовый initData (в реальности придёт от Telegram)
    data = {
        "initData": "query_id=test&user=%7B%22id%22%3A5054943911%2C%22first_name%22%3A%22crsc%22%7D&auth_date=1729789200&hash=test",
        "channelId": "@RoleMind"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, timeout=10)
            print(f"Статус: {response.status_code}")
            print(f"Ответ: {response.json()}")
    except Exception as e:
        print(f"Ошибка: {e}")

asyncio.run(test())

