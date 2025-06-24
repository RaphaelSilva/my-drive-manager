DOCKER_FILE_ROOT := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
MY_APP_NAME := $(notdir $(DOCKER_FILE_ROOT))
USE_SSL ?= false
RABBITMQ_HOST ?= localhost
RABBITMQ_PORT ?= 5672
RABBITMQ_USER ?= guest
RABBITMQ_PASSWORD ?= guest
RABBITMQ_QUEUE_NAME ?= backup_from_queue
RABBITMQ_TOPIC_NAME ?= backup_from_topic
RABBITMQ_ROUTING_KEY ?= backup_from_routing_key
LOG_LEVEL ?= INFO


help: ## Show help for the Makefile
	@echo "This Makefile is used to manage the backup_from application."
	@echo "It requires the following environment variables to be set:"	
	@echo "  - DOCKER_FILE_ROOT:=${DOCKER_FILE_ROOT} # The root directory of the project."
	@echo "  - MY_APP_NAME:=${MY_APP_NAME} # The name of the application."
	@echo "  - USE_SSL:=${USE_SSL} # Whether to use SSL for RabbitMQ connections."
	@echo "  - RABBITMQ_HOST:=${RABBITMQ_HOST} # The RabbitMQ host."
	@echo "  - RABBITMQ_PORT:=${RABBITMQ_PORT} # The RabbitMQ port."
	@echo "  - RABBITMQ_USER:=${RABBITMQ_USER} # The RabbitMQ user."
	@echo "  - RABBITMQ_PASSWORD:=${RABBITMQ_PASSWORD} # The RabbitMQ password."
	@echo "  - RABBITMQ_QUEUE_NAME:=${RABBITMQ_QUEUE_NAME} # The RabbitMQ queue name."
	@echo "  - RABBITMQ_TOPIC_NAME:=${RABBITMQ_TOPIC_NAME} # The RabbitMQ topic name."
	@echo "  - RABBITMQ_ROUTING_KEY:=${RABBITMQ_ROUTING_KEY} # The RabbitMQ routing key."
	@echo "  - LOG_LEVEL:=${LOG_LEVEL} # The log level for the application (e.g., DEBUG, INFO, WARNING, ERROR)."
	@echo "Usage:"
	@echo "  make generate-certificates   # Generate certificates for the backup_from application"
	@echo "  make build                   # Build the Docker image for the backup_from application"
	@echo "  make run-docker              # Run the Docker container for the backup_from application"

generate-certificates: ## Generate certificates for the backup_from application
	cd ${DOCKER_FILE_ROOT}/certs
	@echo "Generating certificates for ${MY_APP_NAME}..."
	openssl genrsa -out ca_key.pem 2048
	@echo "Generating CA certificate for ${MY_APP_NAME}..."
	openssl req -x509 -new -nodes -key ca_key.pem -sha256 -days 365 -out ca_certificate.pem -subj "/CN=${MY_APP_NAME}.ca"
	@echo "Generating server key for ${MY_APP_NAME}..."
	openssl genrsa -out server_key.pem 2048
	@echo "Generating server certificate signing request (CSR) for ${MY_APP_NAME}..."
	openssl req -new -key server_key.pem -out server_csr.pem -subj "/CN=${MY_APP_NAME}.server"
	@echo "Signing server CSR with CA certificate for ${MY_APP_NAME}..."	
	openssl x509 -req -in server_csr.pem -CA ca_certificate.pem -CAkey ca_key.pem -CAcreateserial -out server_certificate.pem -days 365 -sha256

build: generate-certificates ## Build the Docker image for the backup_from application
	@echo "Running build for ${MY_APP_NAME}..."	
	docker build -t ${MY_APP_NAME} ${DOCKER_FILE_ROOT}

run-docker: ## Run the Docker container for the backup_from application
	@echo "Running Docker container for ${MY_APP_NAME}..."
	docker run --rm -it \
		--name ${MY_APP_NAME}.container \
		-e RABBITMQ_HOST=${RABBITMQ_HOST} \
		-e RABBITMQ_PORT=${RABBITMQ_PORT} \
		-e RABBITMQ_USER=${RABBITMQ_USER} \
		-e RABBITMQ_PASSWORD=${RABBITMQ_PASSWORD} \
		-e RABBITMQ_QUEUE_NAME=${RABBITMQ_QUEUE_NAME} \
		-e RABBITMQ_TOPIC_NAME=${RABBITMQ_TOPIC_NAME} \
		-e RABBITMQ_ROUTING_KEY=${RABBITMQ_ROUTING_KEY} \
		-e LOG_LEVEL=${LOG_LEVEL} \
		${MY_APP_NAME}
