FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    firefox-esr \
    xvfb \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install geckodriver
RUN python -c "import geckodriver_autoinstaller; geckodriver_autoinstaller.install()"

# Copy application files
COPY . .

# Create logs directory
RUN mkdir -p logs

# Set environment variables
ENV DISPLAY=:99
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "continuous_stealth_bot.py", "--mode", "single", "--execution-time", "30", "--sleep-time", "5"]