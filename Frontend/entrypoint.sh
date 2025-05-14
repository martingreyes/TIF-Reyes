#!/bin/sh

# Agrega http:// explícitamente y verifica variables
BACKEND_URL="http://${BACKEND_HOST}:${BACKEND_PORT}"

echo "Generando archivo env-config.js con BACKEND_URL=${BACKEND_URL}"

cat <<EOF > /usr/share/nginx/html/assets/env-config.js
window.env = {
  apiUrl: "${BACKEND_URL}"
};
EOF

exec "$@"
