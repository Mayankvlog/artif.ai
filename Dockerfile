FROM python:3.13-slim

WORKDIR /app

# Install system dependencies including MySQL client
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    netcat-traditional \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker cache
COPY requirements-extra.txt .

# Install required Python packages
RUN pip install --no-cache-dir -r requirements-extra.txt

# Copy the application code
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create the entrypoint script
RUN echo '#!/bin/bash\n\
# Wait for database to be ready\n\
if [ ! -z "$MYSQL_HOST" ]; then\n\
  echo "Waiting for MySQL database..."\n\
  while ! nc -z $MYSQL_HOST ${MYSQL_PORT:-3306}; do\n\
    sleep 1\n\
  done\n\
  echo "MySQL database is available"\n\
fi\n\
\n\
# Start Gunicorn\n\
exec gunicorn --bind 0.0.0.0:5000 --workers=2 --reuse-port app:app\n\
' > /app/docker-entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /app/docker-entrypoint.sh

# Expose the port
EXPOSE 5000

# Use the entrypoint script
ENTRYPOINT ["/app/docker-entrypoint.sh"]