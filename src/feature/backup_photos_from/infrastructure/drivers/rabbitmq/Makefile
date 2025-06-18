
drive-rabbitmq-check-env: ## check the environment variables
	@echo "Checking environment variables"
	@echo "TARGET_ORIGIN=$(TARGET_ORIGIN)"
	@echo "TARGET_DESTINATION=$(TARGET_DESTINATION)"
	@echo "LOG_LEVEL=$(LOG_LEVEL)"
	@echo "LOGGER=$(LOGGER)"
	@echo "RABBITMQ_QUEUE_NAME=$(RABBITMQ_QUEUE_NAME)"
	@echo "RABBITMQ_TOPIC_NAME=$(RABBITMQ_TOPIC_NAME)"
	@echo "RABBITMQ_ROUTING_KEY=$(RABBITMQ_ROUTING_KEY)"
	@echo "RABBITMQ_HOST=$(RABBITMQ_HOST)"
	@echo "RABBITMQ_PORT=$(RABBITMQ_PORT)"
	@echo "RABBITMQ_USER=$(RABBITMQ_USER)"
	@echo "RABBITMQ_PASSWORD=$(RABBITMQ_PASSWORD)"
	@echo "HOSTNAME=$(HOSTNAME)"
	@echo "HOST_IPADDRESS=$(HOST_IPADDRESS)"

drive-rabbitmq-new-queue: ## Create a new RabbitMQ instance queue
	@echo "Creating RabbitMQ instance queue..."
	$(PYTHON) -m src.feature.backup_photos_from.infrastructure.drivers.rabbitmq \
		--run new_queue

drive-rabbitmq-clean-queue-all: ## Clean the queue
	./init.sh radmin -f tsv -q list queues name | xargs -I {} ./init.sh radmin delete queue name={}

drive-rabbitmq-clean-queue: ## Clean the queue
	./init.sh radmin delete queue name="${QUEUE_NAME}"

drive-rabbitmq-clean-exchange-all: ## Clean all exchanges
	./init.sh radmin -f tsv -q list exchanges name | grep -v amq | xargs -I {} ./init.sh radmin delete exchange name={}

drive-rabbitmq-clean-exchange: ## Clean the exchange
	./init.sh radmin delete exchange name="${EXCHANGE_NAME}"

drive-rabbitmq-clean-all: clean-queue-all clean-exchange-all  ## Clean all