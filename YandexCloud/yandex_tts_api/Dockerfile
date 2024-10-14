FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    sox \
    libsox-fmt-all \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]