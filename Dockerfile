FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment so run_telegram_bot.py venv check passes
RUN python -m venv /app/venv

# Upgrade pip inside the venv
RUN /app/venv/bin/pip install --upgrade pip

# Install Python dependencies into the venv
COPY requirements.txt .
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Run the bot using the venv Python
CMD ["/app/venv/bin/python", "run_telegram_bot.py"]
