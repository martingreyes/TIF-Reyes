#!/bin/sh

echo "[entrypoint.sh] Generando archivo env.js con BACKEND_HOST=${BACKEND_HOST} y BACKEND_PORT=${BACKEND_PORT}..."

# Valores por defecto (opcional)
: "${BACKEND_HOST:=localhost}"
: "${BACKEND_PORT:=3000}"

# Inyectar variables en el template y generar env.js
envsubst < /usr/share/nginx/html/assets/env.template.js > /usr/share/nginx/html/assets/env.js

echo "[entrypoint.sh] Archivo env.js generado correctamente."

# Ejecutar Nginx
exec "$@"
