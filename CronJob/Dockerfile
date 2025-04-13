FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    git \
    gcc \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    libz-dev && apt-get clean

WORKDIR /app

RUN git clone --filter=blob:none --sparse https://github.com/martingreyes/TIF-Reyes.git . \
    && git sparse-checkout init --cone \
    && git sparse-checkout set CronJob


WORKDIR /app/CronJob

RUN pip install --no-cache-dir -r requirements.txt