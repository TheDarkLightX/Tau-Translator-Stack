# Use a slim Python 3.12 image
FROM python:3.12-slim AS build
WORKDIR /app

# Install curl for downloading Tau
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files to the container
COPY . .

# Download the latest Tau binary from GitHub and make it executable
RUN curl -sL https://github.com/IDNI/tau-lang/releases/latest/download/tau-linux-amd64 \
    -o /usr/local/bin/tau \
    && chmod +x /usr/local/bin/tau

# Expose the port the app will run on
EXPOSE 8000

# Command to run the app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

