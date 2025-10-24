# -*- coding: utf-8 -*-
import asyncio
import httpx

BOT_TOKEN = "8124456836:AAFFo3oEJ7d3JNRDy337rHTe9FDTc4-lE8w"
CHAT_ID = 5054943911  # Ваш chat_id из логов

async def test_send():
    print("Тестирование отправки сообщения...")
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": "Тестовое сообщение от бота!"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, timeout=10)
            result = response.json()
            
            print(f"\nОтвет от API:")
            print(f"OK: {result.get('ok')}")
            
            if not result.get('ok'):
                print(f"Ошибка: {result.get('description')}")
                print(f"Код ошибки: {result.get('error_code')}")
            else:
                print("Сообщение отправлено успешно!")
            
            print(f"\nПолный ответ:")
            print(result)
    
    except Exception as e:
        print(f"Исключение: {e}")

if __name__ == "__main__":
    asyncio.run(test_send())

