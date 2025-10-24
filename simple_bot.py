# -*- coding: utf-8 -*-
"""Простой бот для теста"""
import asyncio
import httpx
import os

BOT_TOKEN = "8124456836:AAFFo3oEJ7d3JNRDy337rHTe9FDTc4-lE8w"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

offset = 0

async def send_message(chat_id, text, reply_markup=None):
    """Отправка сообщения"""
    url = f"{API_URL}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        data["reply_markup"] = reply_markup
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, timeout=10)
        return response.json()

async def handle_start(chat_id, username):
    """Обработчик /start"""
    message = f"""Привет{f', {username}' if username else ''}!

Добро пожаловать в тест "Кто твоя роль в Dota 2?"

Пройди психологический тест и узнай, какая позиция подходит тебе больше всего!

Тест определит твою роль из 5 позиций:
• Керри (Position 1)
• Мидер (Position 2)
• Оффлейнер (Position 3)
• Хардсапорт (Position 4)
• Фулл Саппорт (Position 5)

Нажми кнопку ниже, чтобы начать!"""
    
    # WebApp кнопка
    reply_markup = {
        "inline_keyboard": [
            [
                {
                    "text": "Начать тест",
                    "web_app": {"url": "http://localhost:8000"}
                }
            ]
        ]
    }
    
    result = await send_message(chat_id, message, reply_markup)
    print(f"Отправлено сообщение в чат {chat_id}: {result.get('ok')}")

async def get_updates():
    """Получение обновлений"""
    global offset
    url = f"{API_URL}/getUpdates"
    params = {
        "offset": offset,
        "timeout": 30
    }
    
    async with httpx.AsyncClient(timeout=35) as client:
        response = await client.get(url, params=params)
        return response.json()

async def run_bot():
    """Запуск бота"""
    global offset
    
    print("Бот запущен!")
    print("Ожидание сообщений...\n")
    
    while True:
        try:
            updates = await get_updates()
            
            if not updates.get("ok"):
                print(f"Ошибка API: {updates}")
                await asyncio.sleep(5)
                continue
            
            for update in updates.get("result", []):
                offset = update["update_id"] + 1
                
                if "message" not in update:
                    continue
                
                message = update["message"]
                chat_id = message["chat"]["id"]
                text = message.get("text", "")
                username = message.get("from", {}).get("first_name", "")
                
                print(f"Получено: {text} от {username} (chat_id: {chat_id})")
                
                if text.startswith("/start") or text.startswith("/test"):
                    await handle_start(chat_id, username)
                elif text.startswith("/help"):
                    await send_message(chat_id, "Используй /start чтобы начать тест")
                else:
                    await send_message(chat_id, "Используй /start чтобы начать тест")
        
        except Exception as e:
            print(f"Ошибка: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print("\nБот остановлен")

