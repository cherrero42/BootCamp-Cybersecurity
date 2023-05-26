docker-compose up -d
docker network inspect inquisitor_default | grep -e IPv4 -e Name -e Mac
echo "Connecting to user..."
ssh root@127.0.0.1 -p4141
echo "Connecting to poisoner..."
ssh root@127.0.0.1 -p4242