#!/usr/bin/env python3
import os
import re
import time
import requests
from dotenv import load_dotenv

load_dotenv()

LOG_FILE = os.getenv("LOG_FILE", "/app/logs/access.log")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) - - \[(?P<time>.*?)\] "(?P<method>\S+) (?P<path>\S+) (?P<proto>.*?)" (?P<status>\d{3})'
)

# Защита от спама
last_alert_time = 0

def send_telegram_message(msg: str):
    global last_alert_time

    if not TELEGRAM_TOKEN or not CHAT_ID:
        return

    # Cooldown 2 минуты
    current_time = time.time()
    if current_time - last_alert_time < 120:
        return

    last_alert_time = current_time

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg}, timeout=10)
        print("✅ Telegram alert sent", flush=True)
    except:
        print("❌ Telegram send failed", flush=True)

def process_line(line: str):
    match = LOG_PATTERN.search(line)
    if not match:
        return

    data = match.groupdict()
    status = data["status"]
    timestamp = data["time"]

    # Теперь выводим ВРЕМЯ из лога!
    print(f"{timestamp} | {status} | {data['ip']} | {data['method']} {data['path']}", flush=True)

    if status.startswith('5'):
        alert_msg = f"🚨 5xx ERROR\nTime: {timestamp}\nIP: {data['ip']}\nStatus: {status}\nRequest: {data['method']} {data['path']}"
        send_telegram_message(alert_msg)

def monitor_logs():
    print(f"🔍 Monitoring: {LOG_FILE}", flush=True)

    try:
        with open(LOG_FILE, "r") as f:
            f.seek(0, 2)

            while True:
                line = f.readline()
                if line:
                    process_line(line.strip())
                else:
                    time.sleep(0.1)

    except KeyboardInterrupt:
        print("🛑 Stopped", flush=True)
    except Exception as e:
        print(f"❌ Error: {e}", flush=True)

if __name__ == "__main__":
    monitor_logs()
