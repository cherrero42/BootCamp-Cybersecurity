FROM alpine:latest

RUN set -e -x && apk update && apk add openssh-server lftp

COPY sshd_config /etc/ssh/sshd_config
COPY entrypoint.sh /entrypoint.sh

RUN set -e -x &&  chmod +x /entrypoint.sh && \
    echo "root:root" | chpasswd

WORKDIR /usr/src/

EXPOSE 4141

CMD ["sh", "/entrypoint.sh"]
