# -*- coding: utf-8 -*-
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

if not BOT_TOKEN:
    print("Ошибка: BOT_TOKEN не установлен в .env файле")
    sys.exit(1)

async def setup_bot():
    """Настраивает бота через Telegram Bot API"""
    
    print("Настройка Telegram бота...")
    print(f"Token: {BOT_TOKEN[:10]}...")
    
    async with httpx.AsyncClient() as client:
        # Получаем информацию о боте
        print("\n1. Получение информации о боте...")
        response = await client.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
        )
        data = response.json()
        
        if not data.get('ok'):
            print(f"Ошибка: {data.get('description')}")
            return
        
        bot_info = data['result']
        print(f"   Бот найден: @{bot_info['username']}")
        print(f"   Имя: {bot_info.get('first_name', 'N/A')}")
        
        # Устанавливаем команды бота
        print("\n2. Установка команд бота...")
        commands = [
            {"command": "start", "description": "Начать тест"},
            {"command": "test", "description": "Пройти тест заново"},
            {"command": "help", "description": "Помощь"}
        ]
        
        response = await client.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/setMyCommands",
            json={"commands": commands}
        )
        
        if response.json().get('ok'):
            print("   Команды установлены")
        
        print("\nГотово!")
        print(f"\nСсылка на бота: https://t.me/{bot_info['username']}")
        print(f"\nНе забудьте:")
        print("1. Добавить бота админом в канал для проверки подписки")
        print("2. Настроить WebApp кнопку в боте через @BotFather")

if __name__ == "__main__":
    asyncio.run(setup_bot())

