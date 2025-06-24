#!/bin/bash

HOSTNAME=root
HOST_IPADDRESS=192.168.1.107
HOSTNAME_IPADDRESS=$HOSTNAME@$HOST_IPADDRESS

RABBITMQ_WEBAPI_PORT=15672

echo "Using RabbitMQ host: $HOSTNAME_IPADDRESS"

send_files() {
    echo "Copying docker files..."
    ssh $HOSTNAME_IPADDRESS "mkdir -p /root/dockerfile"
    for folder in ./dockerfile/*; do
        echo "Copying files from $folder to $HOSTNAME_IPADDRESS:/root/dockerfile/"
        scp -r $folder $HOSTNAME_IPADDRESS:/root/dockerfile/
    done
    echo "Building images..."
    scp ./Makefile $HOSTNAME_IPADDRESS:/root/Makefile    
    scp ./docker-compose.yml $HOSTNAME_IPADDRESS:/root/docker-compose.yml
    scp .env $HOSTNAME_IPADDRESS:/root/.env
    echo "Files copied successfully."
    ## ssh $HOSTNAME_IPADDRESS "/root/servers/queue/server.sh init"
}

build() {
    echo "Building the queue service..."
    ssh $HOSTNAME_IPADDRESS "cd /root && make image-services-build"
}

run() {
    echo "Running the queue service..."
    ssh $HOSTNAME_IPADDRESS "/root/servers/queue/server.sh $@"
}

start() {
    echo "Starting the queue service..."
    ssh $HOSTNAME_IPADDRESS "/root/servers/queue/server.sh start"
}

reload() {
    echo "Reloading the queue service..."
    ssh $HOSTNAME_IPADDRESS "/root/servers/queue/server.sh reload"
}
stop() {
    echo "Stopping the queue service..."
    ssh $HOSTNAME_IPADDRESS "/root/servers/queue/server.sh stop"
}

list() {
    curl -i -u ${RABBITMQ_USER}:${RABBITMQ_PASSWORD} -H "content-type:application/json" \
        -XGET http://$HOSTNAME_IPADDRESS:$RABBITMQ_WEBAPI_PORT/api/queues
}

radmin() {
    #echo "Running RabbitMQ admin commands: $@"
    #echo "params: host=${RABBITMQ_HOST} :: web_port_api=${RABBITMQ_WEBAPI_PORT} :: user=${RABBITMQ_USER} :: pass=${RABBITMQ_PASSWORD}"
    rabbitmqadmin \
        -H ${RABBITMQ_HOST} \
        -P ${RABBITMQ_WEBAPI_PORT} \
        -u ${RABBITMQ_USER} \
        -p ${RABBITMQ_PASSWORD} $@
}

$1 ${@:2}
