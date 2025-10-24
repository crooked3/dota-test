# 🚀 Руководство по деплою

## Варианты деплоя

### 1. Vercel (Frontend) + Railway (Backend)

#### Frontend на Vercel:

1. Зарегистрируйтесь на [Vercel](https://vercel.com)
2. Установите Vercel CLI:
```bash
npm install -g vercel
```

3. Деплой фронтенда:
```bash
cd frontend
vercel
```

4. Следуйте инструкциям CLI
5. Получите URL (например, `https://your-app.vercel.app`)

#### Backend на Railway:

1. Зарегистрируйтесь на [Railway](https://railway.app)
2. Создайте новый проект
3. Подключите GitHub репозиторий или деплойте локально
4. Установите переменные окружения:
   - `BOT_TOKEN`
   - `CHANNEL_ID`
5. Railway автоматически определит Python и запустит приложение
6. Получите URL API (например, `https://your-app.railway.app`)

### 2. Netlify (Frontend) + Heroku (Backend)

#### Frontend на Netlify:

1. Зарегистрируйтесь на [Netlify](https://netlify.com)
2. Перетащите папку `frontend/` в Netlify Dashboard
3. Или используйте Netlify CLI:
```bash
npm install -g netlify-cli
cd frontend
netlify deploy --prod
```

#### Backend на Heroku:

1. Зарегистрируйтесь на [Heroku](https://heroku.com)
2. Установите Heroku CLI
3. Создайте Procfile в папке backend:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

4. Деплой:
```bash
cd backend
heroku create your-app-name
heroku config:set BOT_TOKEN=your_token
heroku config:set CHANNEL_ID=@yourchannel
git init
git add .
git commit -m "Initial commit"
git push heroku master
```

### 3. VPS (Ubuntu 22.04)

#### Подготовка сервера:

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка зависимостей
sudo apt install python3-pip python3-venv nginx certbot python3-certbot-nginx -y

# Установка Node.js (для фронтенда, если нужно)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y
```

#### Backend:

```bash
# Клонирование проекта
cd /var/www
sudo git clone your-repo
cd your-repo/backend

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Создание .env файла
sudo nano .env
# Заполните переменные

# Создание systemd сервиса
sudo nano /etc/systemd/system/dota-backend.service
```

Содержимое `dota-backend.service`:
```ini
[Unit]
Description=Dota 2 Role Test Backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/your-repo/backend
Environment="PATH=/var/www/your-repo/backend/venv/bin"
ExecStart=/var/www/your-repo/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 5000

[Install]
WantedBy=multi-user.target
```

```bash
# Запуск сервиса
sudo systemctl daemon-reload
sudo systemctl enable dota-backend
sudo systemctl start dota-backend
sudo systemctl status dota-backend
```

#### Frontend:

```bash
# Копирование файлов
sudo mkdir -p /var/www/dota-frontend
sudo cp -r frontend/* /var/www/dota-frontend/

# Настройка прав
sudo chown -R www-data:www-data /var/www/dota-frontend
```

#### Nginx конфигурация:

```bash
sudo nano /etc/nginx/sites-available/dota-test
```

Содержимое:
```nginx
# Frontend
server {
    listen 80;
    server_name yourdomain.com;

    root /var/www/dota-frontend;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location ~* \.(js|css|json)$ {
        expires 1d;
        add_header Cache-Control "public, immutable";
    }
}

# Backend API
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
# Активация конфигурации
sudo ln -s /etc/nginx/sites-available/dota-test /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Установка SSL сертификатов
sudo certbot --nginx -d yourdomain.com -d api.yourdomain.com
```

### 4. Docker Compose (полный стек)

Создайте `docker-compose.yml` в корне проекта:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
      - CHANNEL_ID=${CHANNEL_ID}
    env_file:
      - .env
    restart: unless-stopped

  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./frontend:/usr/share/nginx/html:ro
    restart: unless-stopped

  bot:
    build: ./config
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
      - WEBAPP_URL=${WEBAPP_URL}
      - CHANNEL_URL=${CHANNEL_URL}
    env_file:
      - .env
    restart: unless-stopped
    depends_on:
      - backend
```

Запуск:
```bash
docker-compose up -d
```

## Обновление конфигурации WebApp

После деплоя обновите URLs в коде:

### 1. Frontend (app.js):
```javascript
const config = {
    channelUrl: 'https://t.me/yourchannel',
    channelId: '@yourchannel',
    backendUrl: 'https://api.yourdomain.com'  // ← обновите
};
```

### 2. Backend (.env):
```env
BOT_TOKEN=your_token_here
CHANNEL_ID=@yourchannel
```

### 3. Telegram Bot (у @BotFather):
- Menu Button URL: `https://yourdomain.com`

## Проверка работоспособности

### Backend:
```bash
curl https://api.yourdomain.com/health
# Ответ: {"status":"healthy"}
```

### Frontend:
Откройте `https://yourdomain.com` в браузере

### WebApp:
1. Откройте бота в Telegram
2. Нажмите кнопку меню
3. Должно открыться приложение

## Мониторинг и логи

### Логи backend (systemd):
```bash
sudo journalctl -u dota-backend -f
```

### Логи Nginx:
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Docker логи:
```bash
docker-compose logs -f backend
```

## Безопасность

✅ **Чеклист безопасности:**

- [ ] HTTPS настроен для фронтенда и бэкенда
- [ ] .env файлы добавлены в .gitignore
- [ ] BOT_TOKEN не светится в коде
- [ ] Настроены правильные CORS origins
- [ ] Backend валидирует все запросы
- [ ] Бот - админ в канале
- [ ] Настроен firewall (ufw/iptables)
- [ ] Регулярные обновления пакетов
- [ ] Бэкапы настроены

## Troubleshooting

### WebApp не открывается:
1. Проверьте HTTPS на фронтенде
2. Проверьте URL в настройках бота
3. Откройте DevTools в Telegram Desktop

### Backend не отвечает:
1. Проверьте статус сервиса: `systemctl status dota-backend`
2. Проверьте логи: `journalctl -u dota-backend -n 50`
3. Проверьте порт: `netstat -tulpn | grep 5000`

### Проверка подписки не работает:
1. Убедитесь, что бот - админ канала
2. Проверьте правильность CHANNEL_ID
3. Проверьте логи backend

## Масштабирование

### Для высоких нагрузок:

1. **Backend:**
   - Используйте несколько инстансов за балансировщиком
   - Добавьте Redis для кеширования
   - Настройте rate limiting

2. **Frontend:**
   - Используйте CDN (Cloudflare, CloudFront)
   - Минифицируйте JS/CSS
   - Оптимизируйте изображения

3. **База данных (если добавите):**
   - PostgreSQL для хранения результатов
   - Индексы для быстрых запросов

## Поддержка

Если возникли проблемы:
1. Проверьте логи
2. Прочитайте документацию Telegram
3. Проверьте issues в репозитории

---

**Успешного деплоя! 🚀**

