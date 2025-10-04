
# 🐳 Nginx Log Monitor with Telegram Alerts

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg?logo=docker)](https://docker.com)
[![Telegram](https://img.shields.io/badge/telegram-bot-26A5E4.svg?logo=telegram)](https://telegram.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**🇺🇸 English** | **🇷🇺 [Russian Version](README.ru.md)**

Real-time Nginx log monitoring with instant Telegram notifications for 5xx server errors. Simple, effective, and ready to use.

## ✨ Features

- 🔍 **Real-time monitoring** - `tail -f` style log parsing
- 📱 **Smart Telegram alerts** - Instant notifications for 5xx errors with cooldown protection
- 🐳 **Docker-ready** - Full containerization with docker-compose
- ⚙️ **Simple configuration** - Environment variables based setup
- 🚀 **Zero setup** - Works out of the box

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Telegram Bot Token ([get from @BotFather](https://t.me/BotFather))
- Telegram Chat ID ([get from @userinfobot](https://t.me/userinfobot))

### Installation & Running

```bash
# 1. Clone and setup
git clone https://github.com/DanLinX2004X/nginx-log-monitor.git
cd nginx-log-monitor

# 2. Configure environment
cp .env.example .env
# Edit .env and add your Telegram token and chat ID

# 3. Launch everything
docker-compose up -d --build

# 4. View monitor logs
docker-compose logs -f monitor
```

### Testing
```bash
# Generate test traffic
curl http://localhost:8080/                    # 200 Success
curl http://localhost:8080/nonexistent-page    # 404 Client Error

# For 5xx testing, you can:
# - Modify Nginx config to return 500 errors
# - Or use the included test endpoint (if available)
```

## 🐳 Docker Services

### Services Overview
- **nginx** - Nginx web server with test page
- **monitor** - Python service that monitors logs and sends Telegram alerts

### Volumes
- `./logs:/var/log/nginx` - Nginx writes logs here
- `./logs:/app/logs` - Monitor reads the same logs (read-only)

### Environment Variables
Configure in `.env` file:
```bash
TELEGRAM_TOKEN=your_bot_token_here
CHAT_ID=your_chat_id_here
# Optional: LOG_FILE=/app/logs/access.log
```

## 🛑 Management

```bash
# Stop and remove containers
docker-compose down

# Stop but keep data
docker-compose stop

# Restart services
docker-compose restart

# View specific service logs
docker-compose logs -f nginx
docker-compose logs -f monitor
```

## 📝 How It Works

1. **Nginx** serves web content and writes access logs to `./logs/access.log`
2. **Monitor** reads logs in real-time using `tail -f` approach
3. **When 5xx error occurs** - sends formatted alert to Telegram
4. **Cooldown protection** - prevents spam for repeated errors

### Example Alert Format
```
🚨 5xx ERROR
Time: 04/Oct/2025:21:30:00 +0000
IP: 127.0.0.1
Status: 500
Request: GET /api/users
```

## 🐛 Troubleshooting

### Telegram Not Working
```bash
# Check if tokens are loaded
docker-compose logs monitor | grep "Telegram"

# Verify .env file
cat .env

# Test Telegram connection
docker exec nginx-monitor python -c "
import os; from dotenv import load_dotenv; load_dotenv()
print('Token:', bool(os.getenv('TELEGRAM_TOKEN')))
print('Chat ID:', bool(os.getenv('CHAT_ID')))
"
```

### No Logs Appearing
```bash
# Check if Nginx is writing logs
docker-compose logs nginx
ls -la logs/

# Verify monitor can see the log file
docker exec nginx-monitor ls -la /app/logs/

# Test Nginx is responding
curl -I http://localhost:8080/
```

### Monitor Container Issues
```bash
# Restart monitor only
docker-compose restart monitor

# Rebuild and restart
docker-compose up -d --build monitor
```

## 📁 Project Structure
```
nginx-log-monitor/
├── docker-compose.yml          # Multi-service setup
├── Dockerfile                  # Monitor container
├── parser.py                   # Main monitoring script
├── requirements.txt            # Python dependencies
├── .env.example               # Configuration template
├── html/                      # Web content
│   └── index.html            # Test page
└── logs/                      # Nginx logs (auto-created)
```

## 🤝 Contributing

Contributions welcome! Feel free to:
- Open issues for bugs or feature requests
- Submit pull requests with improvements
- Star the repo if you find it useful

---

*Simple, effective monitoring without the complexity.*