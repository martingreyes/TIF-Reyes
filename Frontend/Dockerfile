# Etapa 1: Build de Angular
FROM node:18-alpine AS build

WORKDIR /app

RUN apk add --no-cache git

# Clonás solo el frontend
RUN git clone --filter=blob:none --sparse https://github.com/martingreyes/TIF-Reyes.git . \
    && git sparse-checkout init --cone \
    && git sparse-checkout set Frontend

WORKDIR /app/Frontend

RUN npm install -g @angular/cli

RUN npm install
RUN npm run build --prod


# Etapa 2: Imagen final con NGINX
FROM nginx:alpine

# Copiar archivos compilados de Angular
COPY --from=build /app/Frontend/www /usr/share/nginx/html


# Copiar entrypoint y darle permisos
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copiar config de NGINX si querés usar una personalizada
# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
