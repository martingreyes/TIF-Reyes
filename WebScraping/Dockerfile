FROM python:3.10-slim

# Instalar herramientas necesarias
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    libz-dev && apt-get clean

# Crear directorio de trabajo
WORKDIR /app

# Clonar solo la carpeta WebScraping
RUN git clone --filter=blob:none --sparse https://github.com/martingreyes/TIF-Reyes.git . \
    && git sparse-checkout init --cone \
    && git sparse-checkout set WebScraping

# Cambiar al directorio WebScraping
WORKDIR /app/WebScraping

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/WebScraping/marketscraper/marketscraper

# Exponer el puerto de scrapyrt
EXPOSE 9080

# Ejecutar scrapyrt desde el path correcto
CMD ["scrapyrt"]
