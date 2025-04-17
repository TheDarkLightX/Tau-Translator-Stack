FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN curl -sL https://github.com/IDNI/tau-lang/releases/latest/download/tau-linux-amd64 -o /usr/local/bin/tau \
    && chmod +x /usr/local/bin/tau
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
