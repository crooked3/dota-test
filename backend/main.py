# -*- coding: utf-8 -*-
"""
Backend для Telegram WebApp - Тест "Кто твоя роль в Dota 2?"
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hmac
import hashlib
import urllib.parse
import os
from typing import Optional
import httpx
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

app = FastAPI(title="Dota 2 Role Test API")

# CORS для разработки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Конфигурация
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@yourchannel")

# Модели данных
class SubscriptionCheckRequest(BaseModel):
    initData: str
    channelId: Optional[str] = None

class SubscriptionCheckResponse(BaseModel):
    subscribed: bool
    user_id: Optional[int] = None
    username: Optional[str] = None

# Утилиты для валидации Telegram WebApp
def validate_telegram_webapp_data(init_data: str, bot_token: str) -> dict:
    """
    Валидация данных от Telegram WebApp
    Документация: https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app
    """
    try:
        # Парсим init_data
        params = urllib.parse.parse_qs(init_data)
        
        # Извлекаем hash
        received_hash = params.get('hash', [None])[0]
        if not received_hash:
            raise ValueError("No hash provided")
        
        # Создаем строку data_check_string
        data_check_arr = []
        for key in sorted(params.keys()):
            if key != 'hash':
                values = params[key]
                for value in values:
                    data_check_arr.append(f"{key}={value}")
        
        data_check_string = '\n'.join(data_check_arr)
        
        # Создаем secret_key
        secret_key = hmac.new(
            "WebAppData".encode(),
            bot_token.encode(),
            hashlib.sha256
        ).digest()
        
        # Вычисляем hash
        calculated_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Проверяем hash
        if not hmac.compare_digest(calculated_hash, received_hash):
            raise ValueError("Invalid hash")
        
        # Парсим данные пользователя
        import json
        user_data = {}
        if 'user' in params:
            user_json = params['user'][0]
            user_data = json.loads(user_json)
        
        return {
            'valid': True,
            'user': user_data
        }
    
    except Exception as e:
        print(f"Validation error: {e}")
        return {
            'valid': False,
            'error': str(e)
        }

async def check_channel_subscription(user_id: int, channel_id: str, bot_token: str) -> bool:
    """
    Проверка подписки пользователя на канал через Telegram Bot API
    """
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getChatMember"
        params = {
            "chat_id": channel_id,
            "user_id": user_id
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()
            
            if not data.get('ok'):
                print(f"Telegram API error: {data}")
                return False
            
            # Проверяем статус пользователя
            status = data.get('result', {}).get('status', '')
            
            # Считаем подписанным, если статус: creator, administrator, member
            subscribed_statuses = ['creator', 'administrator', 'member']
            return status in subscribed_statuses
    
    except Exception as e:
        print(f"Error checking subscription: {e}")
        return False

# API Endpoints

@app.get("/")
async def root():
    """Корневой эндпоинт для проверки работы API"""
    return {
        "status": "ok",
        "message": "Dota 2 Role Test API is running"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/check-subscription", response_model=SubscriptionCheckResponse)
async def check_subscription(request: SubscriptionCheckRequest):
    """
    Проверка подписки пользователя на канал
    
    1. Валидирует initData от Telegram WebApp
    2. Извлекает user_id
    3. Проверяет подписку через Bot API
    """
    
    # Проверяем наличие токена бота
    if not BOT_TOKEN:
        raise HTTPException(
            status_code=500,
            detail="Bot token not configured"
        )
    
    # Валидируем данные от Telegram
    validation_result = validate_telegram_webapp_data(
        request.initData,
        BOT_TOKEN
    )
    
    if not validation_result.get('valid'):
        raise HTTPException(
            status_code=401,
            detail="Invalid Telegram WebApp data"
        )
    
    # Извлекаем данные пользователя
    user_data = validation_result.get('user', {})
    user_id = user_data.get('id')
    username = user_data.get('username')
    
    if not user_id:
        raise HTTPException(
            status_code=400,
            detail="User ID not found in request"
        )
    
    # Используем переданный channelId или дефолтный
    channel_id = request.channelId or CHANNEL_ID
    
    # Проверяем подписку
    is_subscribed = await check_channel_subscription(
        user_id,
        channel_id,
        BOT_TOKEN
    )
    
    return SubscriptionCheckResponse(
        subscribed=is_subscribed,
        user_id=user_id,
        username=username
    )

@app.post("/validate-init-data")
async def validate_init_data(request: Request):
    """
    Эндпоинт только для валидации initData
    Полезен для тестирования
    """
    body = await request.json()
    init_data = body.get('initData', '')
    
    if not BOT_TOKEN:
        raise HTTPException(
            status_code=500,
            detail="Bot token not configured"
        )
    
    result = validate_telegram_webapp_data(init_data, BOT_TOKEN)
    
    if not result.get('valid'):
        raise HTTPException(
            status_code=401,
            detail=result.get('error', 'Invalid data')
        )
    
    return {
        "valid": True,
        "user": result.get('user')
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        reload=True
    )

