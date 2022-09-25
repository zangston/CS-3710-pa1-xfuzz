FROM caddy:2-alpine

# Add tc
RUN apk add --no-cache iproute2-tc curl

COPY entrypoint.sh /entrypoint.sh
RUN chmod u+rx,go-w /entrypoint.sh && \
        mkdir -p /var/www/html

CMD [ "/entrypoint.sh" ]
