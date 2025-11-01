# 🐳 Мониторинг логов Nginx с уведомлениями в Telegram

[![Версия Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/docker-готов-2496ED.svg?logo=docker)](https://docker.com)
[![Telegram](https://img.shields.io/badge/telegram-бот-26A5E4.svg?logo=telegram)](https://telegram.org)
[![Лицензия](https://img.shields.io/badge/лицензия-MIT-green.svg)](LICENSE)

**🇺🇸 [English Version](README.md)** | **🇷🇺 Русский**

Мониторинг логов Nginx в реальном времени с мгновенными уведомлениями в Telegram о 5xx ошибках сервера. Просто, эффективно и готово к использованию.

## ✨ Возможности

- 🔍 **Мониторинг в реальном времени** - парсинг логов в стиле `tail -f`
- 📱 **Умные уведомления в Telegram** - мгновенные алерты для 5xx ошибок с защитой от спама
- 🐳 **Готовность к Docker** - полная контейнеризация с docker-compose
- ⚙️ **Простая настройка** - конфигурация через переменные окружения
- 🚀 **Нулевая настройка** - работает из коробки

## 🚀 Быстрый старт

### Требования
- Docker и Docker Compose
- Токен Telegram бота ([получить у @BotFather](https://t.me/BotFather))
- ID чата в Telegram ([получить у @userinfobot](https://t.me/userinfobot))

### Установка и запуск

```bash
# 1. Клонирование и настройка
git clone https://github.com/DanLinX2004X/nginx-log-monitor.git
cd nginx-log-monitor

# 2. Настройка окружения
cp .env.example .env
# Отредактируйте .env и добавьте ваш Telegram токен и ID чата

# 3. Запуск всех сервисов
docker-compose up -d --build

# 4. Просмотр логов монитора
docker-compose logs -f monitor
```

### Тестирование
```bash
# Генерация тестового трафика
curl http://localhost:8080/                    # 200 Успех
curl http://localhost:8080/несуществующая-страница    # 404 Ошибка клиента

# Для тестирования 5xx ошибок можно:
# - Изменить конфигурацию Nginx для возврата 500 ошибок
# - Использовать встроенный тестовый эндпоинт (если доступен)
```

## 🐳 Docker сервисы

### Обзор сервисов
- **nginx** - Nginx веб-сервер с тестовой страницей
- **monitor** - Python сервис для мониторинга логов и отправки уведомлений в Telegram

### Тома
- `./logs:/var/log/nginx` - Nginx пишет логи сюда
- `./logs:/app/logs` - Монитор читает те же логи (только чтение)

### Переменные окружения
Настройте в файле `.env`:
```bash
TELEGRAM_TOKEN=ваш_токен_бота
CHAT_ID=ваш_id_чата
# Опционально: LOG_FILE=/app/logs/access.log
```

## 🛑 Управление

```bash
# Остановить и удалить контейнеры
docker-compose down

# Остановить но сохранить данные
docker-compose stop

# Перезапустить сервисы
docker-compose restart

# Просмотр логов конкретного сервиса
docker-compose logs -f nginx
docker-compose logs -f monitor
```

## 📝 Как это работает

1. **Nginx** обслуживает веб-контент и пишет логи доступа в `./logs/access.log`
2. **Монитор** читает логи в реальном времени используя подход `tail -f`
3. **При возникновении 5xx ошибки** - отправляет форматированный алерт в Telegram
4. **Защита от спама** - предотвращает дублирование алертов для повторяющихся ошибок

### Пример формата алерта
```
🚨 5xx ERROR
Time: 04/Oct/2025:21:30:00 +0000
IP: 127.0.0.1
Status: 500
Request: GET /api/users
```

## ⚙️ Обзор CI Пайплайна

Этот проект включает облегченный Continuous Integration (CI) пайплайн на базе GitHub Actions.

### 🛠 Этапы пайплайна:

1. **Установка зависимостей** — Устанавливает зависимости проекта и обновляет pip
2. **Проверка синтаксиса** — Запускает py_compile для проверки корректности кода  
3. **Тест сборки Docker** — Проверяет, что Docker образ собирается успешно
4. **Проверка Compose** — Валидирует корректность docker-compose.yml
5. **Сканирование безопасности** — Базовые проверки на наличие секретов и уязвимостей

### ✅ Автоматизация:
- **Автоматические запуски**: При каждом push или pull request в ветки `main` и `develop`
- **Ручной запуск**: Доступен через интерфейс GitHub Actions
- **Быстрая обратная связь**: Мгновенная проверка изменений кода

## 🐛 Решение проблем

### Telegram не работает
```bash
# Проверить загружены ли токены
docker-compose logs monitor | grep "Telegram"

# Проверить файл .env
cat .env

# Протестировать подключение к Telegram
docker exec nginx-monitor python -c "
import os; from dotenv import load_dotenv; load_dotenv()
print('Token:', bool(os.getenv('TELEGRAM_TOKEN')))
print('Chat ID:', bool(os.getenv('CHAT_ID')))
"
```

### Логи не появляются
```bash
# Проверить пишет ли Nginx логи
docker-compose logs nginx
ls -la logs/

# Проверить видит ли монитор файл логов
docker exec nginx-monitor ls -la /app/logs/

# Проверить отвечает ли Nginx
curl -I http://localhost:8080/
```

### Проблемы с контейнером монитора
```bash
# Перезапустить только монитор
docker-compose restart monitor

# Пересобрать и перезапустить
docker-compose up -d --build monitor
```

## 📁 Структура проекта
```
nginx-log-monitor/
├── docker-compose.yml          # Мульти-сервисная настройка
├── Dockerfile                  # Контейнер монитора
├── parser.py                   # Основной скрипт мониторинга
├── requirements.txt            # Зависимости Python
├── .env.example                # Шаблон конфигурации
├── html/                       # Веб-контент
│   └── index.html              # Тестовая страница
├── .github                     # GitHub Actions CI/CD пайплайны
│   └── /workflows/             
|            └── ci.yml         # Основной CI пайплайн
|──logs/                        # Логи Nginx (создается автоматически)
└── .gitattributes              # Метаданные репозитория
```

## 🤝 Участие в разработке

Вклад приветствуется! Не стесняйтесь:
- Открывать issues для багов или запросов функций
- Отправлять pull requests с улучшениями
- Ставить звезду репозиторию, если проект полезен

---

*Простой и эффективный мониторинг без лишней сложности.*
