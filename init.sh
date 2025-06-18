#!/bin/bash

HOSTNAME=root
HOST_IPADDRESS=192.168.1.107
HOSTNAME_IPADDRESS=$HOSTNAME_IPADDRESS

RABBITMQ_WEBAPI_PORT=15672


main() {
    echo "This is the main function. $1"    
}

copy_files() {
    echo "Copying files..."
    scp ./init/queue/docker-queue.service $HOSTNAME_IPADDRESS:/lib/systemd/system/docker-queue.service
    scp ./init/queue/service.sh $HOSTNAME_IPADDRESS:/root/servers/queue/server.sh
    scp ./init/queue/docker-compose.yml $HOSTNAME_IPADDRESS:/root/servers/queue/docker-compose.yml
    scp ./.env $HOSTNAME_IPADDRESS:/root/servers/queue/.env
    ssh $HOSTNAME_IPADDRESS "chmod +x /root/servers/queue/server.sh"
    echo "Files copied successfully."
    ## ssh $HOSTNAME_IPADDRESS "/root/servers/queue/server.sh init"
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

list(){
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

# main
