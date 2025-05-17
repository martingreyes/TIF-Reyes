#!/bin/sh

cat <<EOF > /usr/share/nginx/html/assets/app.config.json
{
  "backendUrl": "${backendUrl:-http://localhost:5001}/"
}
EOF

exec nginx -g 'daemon off;' 