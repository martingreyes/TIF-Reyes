#!/bin/sh

# Salir si alguna variable requerida no está definida
: "${BACKEND_HOST:?La variable BACKEND_HOST no está definida}"
: "${BACKEND_PORT:?La variable BACKEND_PORT no está definida}"

echo "[entrypoint.sh] Contenido antes de reemplazar:"
cat /usr/share/nginx/html/assets/env.template.js

echo "[entrypoint.sh] Generando archivo env.js con BACKEND_HOST=${BACKEND_HOST} y BACKEND_PORT=${BACKEND_PORT}..."

# Inyectar variables en el template y generar env.js
envsubst < /usr/share/nginx/html/assets/env.template.js > /usr/share/nginx/html/assets/env.js

echo "[entrypoint.sh] Archivo env.js generado correctamente."

# Ejecutar Nginx
exec "$@"
