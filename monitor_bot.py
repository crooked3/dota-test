# -*- coding: utf-8 -*-
"""Мониторинг работы бота в реальном времени"""
import asyncio
import httpx
import time

BOT_TOKEN = "8124456836:AAFFo3oEJ7d3JNRDy337rHTe9FDTc4-lE8w"

async def monitor():
    print("Мониторинг бота запущен...")
    print("Напишите боту /start в Telegram: https://t.me/RoleMind_bot")
    print("Ожидаю новых сообщений...\n")
    
    # Получаем текущий offset
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates")
        data = response.json()
        offset = 0
        if data.get('ok') and data.get('result'):
            last_update = data['result'][-1]
            offset = last_update['update_id'] + 1
            print(f"Стартовый offset: {offset}\n")
    
    # Мониторим новые сообщения
    while True:
        try:
            async with httpx.AsyncClient(timeout=35) as client:
                response = await client.get(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates",
                    params={"offset": offset, "timeout": 30}
                )
                data = response.json()
                
                if data.get('ok'):
                    for update in data.get('result', []):
                        offset = update['update_id'] + 1
                        
                        if 'message' in update:
                            msg = update['message']
                            user = msg.get('from', {})
                            text = msg.get('text', '')
                            chat_id = msg.get('chat', {}).get('id')
                            
                            print(f"[{time.strftime('%H:%M:%S')}] Получено сообщение:")
                            print(f"  От: {user.get('first_name', 'N/A')} (@{user.get('username', 'N/A')})")
                            print(f"  Текст: {text}")
                            print(f"  Chat ID: {chat_id}")
                            
                            # Проверяем ответ бота
                            await asyncio.sleep(2)
                            response2 = await client.get(
                                f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates",
                                params={"offset": offset}
                            )
                            data2 = response2.json()
                            
                            bot_responded = False
                            if data2.get('ok'):
                                for u in data2.get('result', []):
                                    if 'message' in u and u['message'].get('from', {}).get('is_bot'):
                                        bot_responded = True
                            
                            if bot_responded:
                                print("  ✅ БОТ ОТВЕТИЛ!\n")
                            else:
                                print("  ❌ Бот НЕ ответил (возможно не запущен)\n")
        
        except Exception as e:
            print(f"Ошибка: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(monitor())
    except KeyboardInterrupt:
        print("\nМониторинг остановлен")

