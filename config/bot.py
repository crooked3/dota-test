# -*- coding: utf-8 -*-
"""
Простой Telegram бот для WebApp
Обрабатывает команды /start, /test, /help
"""

import os
import asyncio
from dotenv import load_dotenv

try:
    import httpx
except ImportError:
    print("❌ Установите httpx: pip install httpx")
    exit(1)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
WEBAPP_URL = os.getenv("WEBAPP_URL", "")
CHANNEL_URL = os.getenv("CHANNEL_URL", "https://t.me/yourchannel")

if not BOT_TOKEN:
    print("❌ Ошибка: BOT_TOKEN не установлен в .env")
    exit(1)

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.api_url = f"https://api.telegram.org/bot{token}"
        self.offset = 0
    
    async def send_message(self, chat_id, text, reply_markup=None):
        """Отправка сообщения"""
        url = f"{self.api_url}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        if reply_markup:
            data["reply_markup"] = reply_markup
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            return response.json()
    
    async def get_updates(self):
        """Получение обновлений"""
        url = f"{self.api_url}/getUpdates"
        params = {
            "offset": self.offset,
            "timeout": 30
        }
        
        async with httpx.AsyncClient(timeout=35) as client:
            response = await client.get(url, params=params)
            return response.json()
    
    async def handle_start(self, chat_id, username):
        """Обработчик команды /start"""
        message = f"""
👋 Привет{f', {username}' if username else ''}!

Добро пожаловать в тест <b>"Кто твоя роль в Dota 2?"</b>

🎮 Пройди психологический тест и узнай, какая позиция подходит тебе больше всего!

📊 Тест определит твою роль из 5 позиций:
• Керри (Position 1)
• Мидер (Position 2)
• Оффлейнер (Position 3)
• Хардсапорт (Position 4)
• Фулл Саппорт (Position 5)

Нажми кнопку ниже, чтобы начать! 👇
"""
        
        # Создаем inline клавиатуру с WebApp кнопкой
        reply_markup = {
            "inline_keyboard": [
                [
                    {
                        "text": "🎮 Начать тест",
                        "web_app": {"url": WEBAPP_URL}
                    }
                ],
                [
                    {
                        "text": "📢 Подписаться на канал",
                        "url": CHANNEL_URL
                    }
                ]
            ]
        }
        
        await self.send_message(chat_id, message, reply_markup)
    
    async def handle_help(self, chat_id):
        """Обработчик команды /help"""
        message = """
ℹ️ <b>Помощь</b>

<b>Команды:</b>
/start - Начать тест
/test - Пройти тест заново
/help - Показать это сообщение

<b>О тесте:</b>
Тест состоит из 10 вопросов, которые помогут определить твою роль в Dota 2 на основе психологических предпочтений и стиля игры.

<b>Роли в Dota 2:</b>
• <b>Pos 1 (Керри)</b> - основной damage dealer
• <b>Pos 2 (Мид)</b> - лидер и координатор
• <b>Pos 3 (Оффлейн)</b> - инициатор и танк
• <b>Pos 4 (Хардсапорт)</b> - роумер и контролер
• <b>Pos 5 (Саппорт)</b> - основная поддержка

❓ Вопросы? Напишите нам: {CHANNEL_URL}
"""
        await self.send_message(chat_id, message)
    
    async def process_update(self, update):
        """Обработка одного обновления"""
        if "message" not in update:
            return
        
        message = update["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "")
        username = message.get("from", {}).get("first_name", "")
        
        print(f"📩 Сообщение от {username} ({chat_id}): {text}")
        
        if text.startswith("/start"):
            await self.handle_start(chat_id, username)
        elif text.startswith("/test"):
            await self.handle_start(chat_id, username)
        elif text.startswith("/help"):
            await self.handle_help(chat_id)
        else:
            await self.send_message(
                chat_id,
                "Используй /start чтобы начать тест или /help для помощи"
            )
    
    async def run(self):
        """Запуск бота"""
        print("🤖 Бот запущен!")
        print(f"   WebApp URL: {WEBAPP_URL}")
        print("   Ожидание сообщений...\n")
        
        while True:
            try:
                updates = await self.get_updates()
                
                if not updates.get("ok"):
                    print(f"❌ Ошибка API: {updates}")
                    await asyncio.sleep(5)
                    continue
                
                for update in updates.get("result", []):
                    self.offset = update["update_id"] + 1
                    await self.process_update(update)
            
            except Exception as e:
                print(f"❌ Ошибка: {e}")
                await asyncio.sleep(5)

async def main():
    if not WEBAPP_URL:
        print("⚠️  WEBAPP_URL не установлен. Бот будет работать без WebApp кнопки.")
    
    bot = TelegramBot(BOT_TOKEN)
    await bot.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен")

