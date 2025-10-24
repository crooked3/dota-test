# -*- coding: utf-8 -*-
"""Тестовый скрипт для проверки работы бота"""
import asyncio
import httpx

BOT_TOKEN = "8124456836:AAFFo3oEJ7d3JNRDy337rHTe9FDTc4-lE8w"

async def test_bot():
    print("Тестирование бота...")
    
    async with httpx.AsyncClient() as client:
        # Проверяем токен
        print("\n1. Проверка токена...")
        response = await client.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getMe")
        data = response.json()
        
        if data.get('ok'):
            bot_info = data['result']
            print(f"   ОК! Бот: @{bot_info['username']}")
            print(f"   Имя: {bot_info['first_name']}")
        else:
            print(f"   ОШИБКА: {data}")
            return
        
        # Проверяем получение обновлений
        print("\n2. Получение последних обновлений...")
        response = await client.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates")
        data = response.json()
        
        if data.get('ok'):
            updates = data.get('result', [])
            print(f"   Получено обновлений: {len(updates)}")
            
            if updates:
                print("\n   Последние сообщения:")
                for update in updates[-3:]:  # Показываем последние 3
                    if 'message' in update:
                        msg = update['message']
                        user = msg.get('from', {})
                        text = msg.get('text', '')
                        print(f"   - От {user.get('first_name', 'N/A')}: {text}")
            else:
                print("   Обновлений нет. Попробуйте написать боту /start")
        else:
            print(f"   ОШИБКА: {data}")
        
        print("\n3. Проверка команд...")
        response = await client.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getMyCommands")
        data = response.json()
        
        if data.get('ok'):
            commands = data.get('result', [])
            if commands:
                print("   Установленные команды:")
                for cmd in commands:
                    print(f"   - /{cmd['command']}: {cmd['description']}")
            else:
                print("   Команды не установлены")
        
        print("\nБот работает! Напишите ему /start в Telegram: https://t.me/RoleMind_bot")

if __name__ == "__main__":
    asyncio.run(test_bot())

