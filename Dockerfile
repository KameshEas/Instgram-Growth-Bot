FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (including psutil for health checks)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Health check: runs every 30s, waits 10s for response, fails after 3 attempts
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python healthcheck.py

# Run the bot
CMD ["python", "run_telegram_bot.py"]
