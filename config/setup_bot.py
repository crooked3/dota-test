# -*- coding: utf-8 -*-
"""
Скрипт для настройки Telegram бота с WebApp
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

try:
    import httpx
except ImportError:
    print("Установите httpx: pip install httpx")
    sys.exit(1)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
WEBAPP_URL = os.getenv("WEBAPP_URL", "")
BOT_USERNAME = os.getenv("BOT_USERNAME", "")

if not BOT_TOKEN:
    print("❌ Ошибка: BOT_TOKEN не установлен в .env файле")
    sys.exit(1)

if not WEBAPP_URL:
    print("❌ Ошибка: WEBAPP_URL не установлен в .env файле")
    sys.exit(1)

async def setup_bot():
    """Настраивает бота через Telegram Bot API"""
    
    print("🤖 Настройка Telegram бота...")
    print(f"   Token: {BOT_TOKEN[:10]}...")
    print(f"   WebApp URL: {WEBAPP_URL}")
    
    async with httpx.AsyncClient() as client:
        # Получаем информацию о боте
        print("\n1. Получение информации о боте...")
        response = await client.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
        )
        data = response.json()
        
        if not data.get('ok'):
            print(f"❌ Ошибка: {data.get('description')}")
            return
        
        bot_info = data['result']
        print(f"   ✓ Бот найден: @{bot_info['username']}")
        print(f"   Имя: {bot_info.get('first_name', 'N/A')}")
        
        # Устанавливаем команды бота
        print("\n2. Установка команд бота...")
        commands = [
            {
                "command": "start",
                "description": "Начать тест"
            },
            {
                "command": "test",
                "description": "Пройти тест заново"
            },
            {
                "command": "help",
                "description": "Помощь"
            }
        ]
        
        response = await client.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/setMyCommands",
            json={"commands": commands}
        )
        
        if response.json().get('ok'):
            print("   ✓ Команды установлены")
        
        # Устанавливаем описание бота
        print("\n3. Установка описания бота...")
        
        description_ru = """
Психологический тест для определения твоей роли в Dota 2!

🎮 10 вопросов
🎯 5 позиций (Pos1-Pos5)
📊 Детальная статистика

Нажми /start чтобы начать!
"""
        
        response = await client.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/setMyDescription",
            json={"description": description_ru, "language_code": "ru"}
        )
        
        if response.json().get('ok'):
            print("   ✓ Описание установлено (RU)")
        
        description_en = """
Psychological test to find your Dota 2 role!

🎮 10 questions
🎯 5 positions (Pos1-Pos5)
📊 Detailed statistics

Press /start to begin!
"""
        
        response = await client.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/setMyDescription",
            json={"description": description_en, "language_code": "en"}
        )
        
        if response.json().get('ok'):
            print("   ✓ Описание установлено (EN)")
        
        print("\n✅ Настройка завершена!")
        print(f"\n📱 Ссылка на бота: https://t.me/{bot_info['username']}")
        print(f"\n⚠️  Не забудьте:")
        print("   1. Добавить бота админом в канал для проверки подписки")
        print("   2. Настроить WebApp кнопку в боте")
        print("   3. Развернуть фронтенд и бэкенд на серверах")

if __name__ == "__main__":
    asyncio.run(setup_bot())

