FROM node:18-alpine AS builder

WORKDIR /app

RUN apk add --no-cache git
RUN git clone --filter=blob:none --sparse https://github.com/martingreyes/TIF-Reyes.git . \
    && git sparse-checkout init --cone \
    && git sparse-checkout set Frontend

    
RUN npm run build -- --configuration=production

RUN npm install && npm run build --prod

FROM nginx:alpine
COPY --from=builder /app/www /usr/share/nginx/html

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 80
ENTRYPOINT ["/entrypoint.sh"]