# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Create log and static directories
RUN mkdir -p /app/log /app/static && chmod 777 /app/log /app/static

# Expose port
EXPOSE ${PORT:-8000}

# Default commands
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "collectstatic", "--noinput"]
CMD ["gunicorn", "-c", "config.py", "trainer.wsgi"]
