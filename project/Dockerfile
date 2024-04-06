FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

COPY project /app/project

# Install dependencies
COPY requirements.txt /app/project/requirements.txt
RUN pip install --no-cache-dir -r /app/project/requirements.txt

ENV DJANGO_ALLOWED_HOSTS=${DJANGO_ALLOWED_HOSTS}

WORKDIR /app/project

EXPOSE 9000
