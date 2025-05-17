FROM node:18-alpine AS builder
WORKDIR /app

# Clona el repositorio (según tu configuración actual)
RUN apk add --no-cache git
RUN git clone --filter=blob:none --sparse https://github.com/martingreyes/TIF-Reyes.git . \
    && git sparse-checkout init --cone \
    && git sparse-checkout set Frontend

WORKDIR /app/Frontend

# Instala dependencias
RUN npm install -g @angular/cli
RUN npm install

# Argumento para la URL de la API (se pasa en el build)
ARG API_URL
# Reemplaza el marcador en environment.prod.ts
RUN sed -i "s|\${API_URL}|${API_URL}|g" src/environments/environment.prod.ts
                        
# Build de Angular para producción
RUN npm run build --prod

# --- Etapa 2: Servir con Nginx ---
FROM nginx:alpine

# Copia los archivos built de Angular
COPY --from=builder /app/Frontend/www /usr/share/nginx/html

# Configuración de Nginx (opcional, según tu necesidad)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]