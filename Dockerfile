# PTC Library Admin Dashboard - Simplified Dockerfile
FROM python:3.11-slim

# Set environment variables
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONIOENCODING=UTF-8 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    REFLEX_ENV=prod

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20.x (required for Reflex)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Upgrade pip and install Reflex
RUN pip install --upgrade pip && \
    pip install "reflex==0.8.16"

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set home directory to /app (reflex needs to write config files)
ENV HOME=/app

# Expose ports
EXPOSE 3000 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:3000/ || exit 1

# Run Reflex in production mode
CMD ["reflex", "run", "--env", "prod", "--loglevel", "info"]
