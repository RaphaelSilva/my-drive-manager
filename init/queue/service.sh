#!/bin/bash
ROOT_DIR="/root/servers/queue"

start() {
    echo "Initializing queue service setup..."    
    docker compose -f $ROOT_DIR/docker-compose.yml up -d
}

reload() {
    echo "Reloading systemd..."
    docker compose --env-file $ROOT_DIR/.env -f $ROOT_DIR/docker-compose.yml down
    docker compose --env-file $ROOT_DIR/.env -f $ROOT_DIR/docker-compose.yml up -d
}

stop() {
    echo "Stopping queue service..."
    docker compose -f $ROOT_DIR/docker-compose.yml down
}

create_service_file() {
    if [ -f /lib/systemd/system/docker-queue.service ]; then
        echo "Service file already exists."
        echo "Do you want to overwrite it? (y/n)"        
        read -p "---" -n 1 -r
        echo    # (optional) move to a new line after the input
        if [[ $REPLY =~ ^[Yy]$ ]]
        then
            echo "Overwriting service file..."            
            systemctl stop docker-queue.service || true
            if systemctl is-active --quiet docker-queue.service; then
                echo "Service is still running. Please stop it before overwriting."
                return
            fi
            echo "Service is not running. Proceeding with overwriting."
            systemctl disable docker-queue.service || true
            rm -f /lib/systemd/system/docker-queue.service
            echo "Service file removed."
        else
            echo "Service file creation aborted."
            return
        fi
    fi
    echo "Creating systemd service file..."
    cat <<EOF > /lib/systemd/system/docker-queue.service
[Unit]
Description=Docker Queue Service
After=docker.service
[Service]
Type=simple
ExecStart=$ROOT_DIR/server.sh start
ExecStop=$ROOT_DIR/server.sh stop
ExecReload=$ROOT_DIR/server.sh reload
Restart=on-failure
RestartSec=5s
User=root
Group=root
WorkingDirectory=$ROOT_DIR
[Install]
WantedBy=multi-user.target
EOF
    echo "Service file created."
    chmod 644 /lib/systemd/system/docker-queue.service
    systemctl daemon-reload
    systemctl enable docker-queue.service
    systemctl start docker-queue.service
    echo "Service enabled and started."
    systemctl status docker-queue.service
    if systemctl is-active --quiet docker-queue.service; then
        echo "Queue service is running."
    else
        echo "Queue service failed to start."
        exit 1
    fi 
}

init() {
    echo "Initializing queue service..."
    create_service_file
    start
}

ok() {
    echo "Queue service is running."
}

if [[ "$1" == "init" ]]; then
    init ${@:2}
elif [[ "$1" == "ok" ]]; then
    ok ${@:2}
elif [[ "$1" == "start" ]]; then
    start ${@:2}
elif [[ "$1" == "reload" ]]; then
    reload ${@:2}
elif [[ "$1" == "stop" ]]; then
    stop ${@:2}
else
    echo "Usage: $0 {init|start|reload|stop}"
    exit 1
fi