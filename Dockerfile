FROM python:3.11-slim

LABEL maintainer="DanLinX2004X" \
      version="1.0" \
      description="Nginx log monitor with Telegram alerts (pet-project fast setup)"


WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY parser.py .

CMD ["python", "parser.py"]
