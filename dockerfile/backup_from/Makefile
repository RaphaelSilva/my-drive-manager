PROJECT_ROOT := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
RABBITMQ_HOST ?= localhost
RABBITMQ_PORT ?= 5672
RABBITMQ_USER ?= guest
RABBITMQ_PASSWORD ?= guest
RABBITMQ_QUEUE_NAME ?= backup_from_queue
RABBITMQ_TOPIC_NAME ?= backup_from_topic
RABBITMQ_ROUTING_KEY ?= backup_from_routing_key
LOG_LEVEL ?= INFO

MY_APP_NAME="backup_from"

help: ## Show help for the Makefile
	@echo "This Makefile is used to manage the backup_from application."
	@echo "It requires the following environment variables to be set:"	
	@echo "  - PROJECT_ROOT: The root directory of the project. ${PROJECT_ROOT}"
	@echo "  - MY_APP_NAME: The name of the application. ${MY_APP_NAME}"
	@echo "  - RABBITMQ_HOST: The RabbitMQ host. ${RABBITMQ_HOST}"
	@echo "  - RABBITMQ_PORT: The RabbitMQ port. ${RABBITMQ_PORT}"
	@echo "  - RABBITMQ_USER: The RabbitMQ user. ${RABBITMQ_USER}"
	@echo "  - RABBITMQ_PASSWORD: The RabbitMQ password. ${RABBITMQ_PASSWORD}"
	@echo "  - RABBITMQ_QUEUE_NAME: The RabbitMQ queue name. ${RABBITMQ_QUEUE_NAME}"
	@echo "  - RABBITMQ_TOPIC_NAME: The RabbitMQ topic name. ${RABBITMQ_TOPIC_NAME}"
	@echo "  - RABBITMQ_ROUTING_KEY: The RabbitMQ routing key. ${RABBITMQ_ROUTING_KEY}"
	@echo "  - LOG_LEVEL: The log level for the application (e.g., DEBUG, INFO, WARNING, ERROR). ${LOG_LEVEL}"
	@echo "Usage:"
	@echo "  make generate-certificates   # Generate certificates for the backup_from application"
	@echo "  make build                   # Build the Docker image for the backup_from application"
	@echo "  make run-docker              # Run the Docker container for the backup_from application"

build: ## Build the Docker image for the backup_from application
	@echo "Running build for ${MY_APP_NAME}..."

run-docker: ## Run the Docker container for the backup_from application
	@echo "Running Docker container for ${MY_APP_NAME}..."
	
