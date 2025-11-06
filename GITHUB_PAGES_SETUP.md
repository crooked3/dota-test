# Развертывание на GitHub Pages + Railway

## 1. Frontend на GitHub Pages

GitHub Actions автоматически деплоит папку `frontend` на GitHub Pages.

**Сайт будет доступен по адресу:**
```
https://crooked3.github.io/dota-test/
```

## 2. Backend на Railway

### Шаг 1: Подготовка репозитория
```bash
cd backend
# Создаем Procfile для Railway
echo "web: gunicorn -w 4 -b 0.0.0.0:\$PORT main:app" > Procfile
# или для uvicorn:
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile
```

### Шаг 2: Создайте Procfile в корне backend/
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Шаг 3: Развертывание на Railway
1. Перейди на https://railway.app
2. Нажми "Start a New Project"
3. Выбери "Deploy from GitHub repo"
4. Подключи свой GitHub аккаунт и выбери репозиторий `dota-test`
5. Выбери ветку `main` и папку `backend`
6. Добавь переменные окружения (Environment):
   ```
   BOT_TOKEN=твой_токен_бота
   CHANNEL_ID=@RoleMind
   ```
7. Railway автоматически развернет приложение

### Шаг 4: Получи URL бэкенда
После развертывания Railway даст тебе URL, например:
```
https://your-dota-backend-production.up.railway.app
```

### Шаг 5: Обнови app.js
```javascript
backendUrl: 'https://your-dota-backend-production.up.railway.app'
```

И затем сделай git push. GitHub Actions автоматически задеплоит фронтенд.

## Итого:
- 🌐 Frontend: https://crooked3.github.io/dota-test/
- ⚙️ Backend: https://your-dota-backend-production.up.railway.app

