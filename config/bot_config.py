# -*- coding: utf-8 -*-
"""
Конфигурация Telegram бота для WebApp
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot настройки
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
BOT_USERNAME = os.getenv("BOT_USERNAME", "")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@yourchannel")
CHANNEL_URL = os.getenv("CHANNEL_URL", "https://t.me/yourchannel")

# WebApp URL
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://yourdomain.com")

# Backend API URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5000")

# Проверка обязательных переменных
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не установлен в .env файле")

print(f"✓ Конфигурация загружена")
print(f"  Bot Username: {BOT_USERNAME}")
print(f"  Channel ID: {CHANNEL_ID}")
print(f"  WebApp URL: {WEBAPP_URL}")
print(f"  Backend URL: {BACKEND_URL}")

