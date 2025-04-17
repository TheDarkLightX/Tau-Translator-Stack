# backend/Dockerfile
FROM python:3.12-slim AS build
WORKDIR /app

# install curl for the tau binary download
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy source AFTER deps to leverage layer cache
COPY . .

# download latest Tau release binary
RUN curl -sL https://github.com/IDNI/tau-lang/releases/latest/download/tau-linux-amd64 \
    -o /usr/local/bin/tau \
    && chmod +x /usr/local/bin/tau

# expose port and run
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

