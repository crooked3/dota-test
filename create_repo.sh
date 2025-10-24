#!/bin/bash
echo "Создание репозитория на GitHub..."

# Авторизация
echo "Stormloh00s123S" | gh auth login --with-token

# Создание репозитория
gh repo create dota-test --public --source=. --push

echo "Готово! Репозиторий: https://github.com/crooked3/dota-test"

