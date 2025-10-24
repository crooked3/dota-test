@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Запуск бота...
python bot_with_logs.py
pause

