# -*- coding: utf-8 -*-
import asyncio
import httpx
from datetime import datetime

BOT_TOKEN = "8124456836:AAFFo3oEJ7d3JNRDy337rHTe9FDTc4-lE8w"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
LOG_FILE = "bot_log.txt"

def log(message):
    """Логирование в файл и консоль"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_message + "\n")

offset = 0

async def send_message(chat_id, text, reply_markup=None):
    """Отправка сообщения"""
    url = f"{API_URL}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_markup:
        data["reply_markup"] = reply_markup
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, timeout=10)
        result = response.json()
        log(f"Отправка сообщения в {chat_id}: {'OK' if result.get('ok') else 'FAIL'}")
        return result

async def handle_start(chat_id, username):
    """Обработчик /start"""
    log(f"Обработка /start от {username} (chat_id: {chat_id})")
    
    message = f"""Привет{f', {username}' if username else ''}!

Добро пожаловать в тест "Кто твоя роль в Dota 2?"

Пройди психологический тест и узнай какая позиция подходит тебе больше всего!

Тест определит твою роль из 5 позиций:
• Керри (Position 1)
• Мидер (Position 2)  
• Оффлейнер (Position 3)
• Хардсапорт (Position 4)
• Фулл Саппорт (Position 5)

Нажми кнопку ниже чтобы начать!"""
    
    # Пока WebApp на localhost - отправляем без кнопки
    # После деплоя раскомментируйте и укажите реальный URL
    # reply_markup = {
    #     "inline_keyboard": [[
    #         {"text": "🎮 Начать тест", "web_app": {"url": "https://your-domain.com"}}
    #     ]]
    # }
    
    message += "\n\n⚠️ Бот готов к работе!"
    message += "\n📱 Для полноценной работы нужно развернуть WebApp на публичном HTTPS домене."
    message += "\n\nПодробности в README.md"
    
    await send_message(chat_id, message)

async def get_updates():
    """Получение обновлений"""
    global offset
    url = f"{API_URL}/getUpdates"
    params = {"offset": offset, "timeout": 30}
    
    async with httpx.AsyncClient(timeout=35) as client:
        response = await client.get(url, params=params)
        return response.json()

async def run_bot():
    """Запуск бота"""
    global offset
    
    log("=== БОТ ЗАПУЩЕН ===")
    log("Ожидание сообщений...")
    log("Напишите боту: https://t.me/RoleMind_bot")
    
    while True:
        try:
            updates = await get_updates()
            
            if not updates.get("ok"):
                log(f"Ошибка API: {updates}")
                await asyncio.sleep(5)
                continue
            
            for update in updates.get("result", []):
                offset = update["update_id"] + 1
                
                if "message" not in update:
                    continue
                
                message = update["message"]
                chat_id = message["chat"]["id"]
                text = message.get("text", "")
                user = message.get("from", {})
                username = user.get("first_name", "")
                
                log(f"Получено сообщение: '{text}' от {username} (@{user.get('username', 'N/A')})")
                
                if text.startswith("/start") or text.startswith("/test"):
                    await handle_start(chat_id, username)
                elif text.startswith("/help"):
                    await send_message(chat_id, "Используй /start чтобы начать тест")
                else:
                    await send_message(chat_id, "Используй /start чтобы начать тест")
        
        except Exception as e:
            log(f"ОШИБКА: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        log("=== БОТ ОСТАНОВЛЕН ===")

