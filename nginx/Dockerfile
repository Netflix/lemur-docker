FROM nginx:1.18.0-alpine

# generate cert on build stage instead of entrypoint
RUN apk add --upgrade --no-cache openssl && mkdir -p /etc/nginx/ssl/ && \
    openssl req -x509 -newkey rsa:4096 -nodes -keyout \
    /etc/nginx/ssl/server.key -out /etc/nginx/ssl/server.crt \
    -days 365 -subj "/C=US/ST=FAKE/L=FAKE/O=FAKE/OU=FAKE/CN=FAKE"

COPY files/lemur-http.conf /etc/nginx/conf.d/lemur-http.conf
COPY files/lemur-ssl.conf /etc/nginx/conf.d/lemur-ssl.conf

CMD ["nginx", "-g", "daemon off;"]