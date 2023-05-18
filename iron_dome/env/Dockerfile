FROM ubuntu:latest   

RUN set -x -e && apt-get update && \
    apt-get install openssh-server -y && apt-get install vim sudo python3 pip libmagic1 -y

COPY sshd_config /etc/ssh/sshd_config
COPY ssh.sh /ssh.sh
COPY requirements.txt /tmp/

RUN set -x -e && pip3 install --requirement /tmp/requirements.txt && \
    chmod +x /ssh.sh && \
    echo "root:root" | chpasswd

RUN useradd -m probe && \
    echo "probe:123456" | chpasswd && \
    groupadd sshusers && \
    usermod -aG sshusers probe && \
    usermod -aG sudo probe

EXPOSE 4141

CMD ["sh", "/ssh.sh"]
