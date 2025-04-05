# Dockerfile
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    netcat gcc postgresql-client && \
    apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Collect static files (optional)
# RUN python manage.py collectstatic --noinput

# Run the application
CMD ["gunicorn", "RBAC.wsgi:application", "--bind", "0.0.0.0:8000"]
