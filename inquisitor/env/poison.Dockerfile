FROM alpine:latest
LABEL maintainer="inquisitor"

RUN set -ex && apk add --update --no-cache net-tools arping python3 py3-pip openssh-server

COPY requirements.txt /tmp/
RUN echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config
# COPY sshd_config /etc/ssh/sshd_config
COPY entrypoint.sh /entrypoint.sh

RUN set -ex && pip3 install --requirement /tmp/requirements.txt && \
    chmod +x /entrypoint.sh 
    # && \     echo "root:root" | chpasswd

WORKDIR /usr/src/

EXPOSE 4141

ENTRYPOINT ["/entrypoint.sh"]

