FROM python:3.10-slim

RUN apt-get update && apt-get install -y gcc libffi-dev libxml2-dev libxslt1-dev libz-dev && apt-get clean

# Crear el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY . /app

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto de scrapyrt
EXPOSE 9080

# Comando para iniciar scrapyrt
CMD ["scrapyrt"]
