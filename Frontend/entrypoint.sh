#!/bin/sh

cat <<EOF > /usr/share/nginx/html/assets/env-config.js
window.env = {
  apiUrl: "${API_URL}"
};
EOF

exec "$@"
