
# Makefile for RabbitMQ driver
drive-rabbitmq-new-queue:
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