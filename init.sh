#!/bin/bash

HOSTNAME=root
IPADDRESS=192.168.1.107

main() {
    echo "This is the main function. $1"    
}

copy_files() {
    echo "Copying files..."
    scp ./init/queue/docker-queue.service $HOSTNAME@$IPADDRESS:/lib/systemd/system/docker-queue.service
    scp ./init/queue/service.sh $HOSTNAME@$IPADDRESS:/root/servers/queue/server.sh
    scp ./init/queue/docker-compose.yml $HOSTNAME@$IPADDRESS:/root/servers/queue/docker-compose.yml
    ssh $HOSTNAME@$IPADDRESS "chmod +x /root/servers/queue/server.sh"
    echo "Files copied successfully."
    ## ssh $HOSTNAME@$IPADDRESS "/root/servers/queue/server.sh init"
}

run() {
    echo "Running the queue service..."
    ssh $HOSTNAME@$IPADDRESS "/root/servers/queue/server.sh $@"
}

start() {
    echo "Starting the queue service..."
    ssh $HOSTNAME@$IPADDRESS "/root/servers/queue/server.sh start"
}

reload() {
    echo "Reloading the queue service..."
    ssh $HOSTNAME@$IPADDRESS "/root/servers/queue/server.sh reload"
}
stop() {
    echo "Stopping the queue service..."
    ssh $HOSTNAME@$IPADDRESS "/root/servers/queue/server.sh stop"
}

list(){
    curl -i -u user:password -H "content-type:application/json" \
    -XGET http://$HOSTNAME@$IPADDRESS:15672/api/queues >> /tmp/queues.json
}

radmin() {
    #echo "Running RabbitMQ admin commands: $@"
    rabbitmqadmin -H 192.168.1.107 -P 15672 -u user -p password $@
}

$1 ${@:2}

# main
