start-backup-from-icloud-photos-info:
	@echo "This Makefile is used to start the backup from iCloud Photos."
	@echo "It requires the following environment variables to be set:"
	@echo "  - TARGET_ORIGIN: The origin path for the backup."
	@echo "  - TARGET_DESTINATION: The destination path for the backup."
	@echo "  - LOG_LEVEL: The log level for the backup process (e.g., DEBUG, INFO, WARNING, ERROR)."
	@echo "Usage: make start-backup-from-icloud-photos"
	@echo "Environment variables:"
	@echo "  TARGET_ORIGIN: $(TARGET_ORIGIN)"
	@echo "  TARGET_DESTINATION: $(TARGET_DESTINATION)"
	@echo "  LOG_LEVEL: $(LOG_LEVEL)"

start-backup-from-icloud-photos: ## Start backup from iCloud Photos
	@echo "Starting backup from iCloud Photos"
	RABBITMQ_HOST=$(RABBITMQ_HOST) \
	RABBITMQ_PORT=$(RABBITMQ_PORT) \
	RABBITMQ_USER=$(RABBITMQ_USER) \
	RABBITMQ_PASSWORD=$(RABBITMQ_PASSWORD) \
	RABBITMQ_QUEUE_NAME=$(RABBITMQ_QUEUE_NAME) \
	RABBITMQ_TOPIC_NAME=$(RABBITMQ_TOPIC_NAME) \
	RABBITMQ_ROUTING_KEY=$(RABBITMQ_ROUTING_KEY) \
	$(PYTHON) -m src.entry.functions.start_backup_from_icloud_photos \
		--function list_all_files_into_queue \
		--origin $(TARGET_ORIGIN) \
		--destination $(TARGET_DESTINATION) \
		--log-level $(LOG_LEVEL)
	@echo "Backup from iCloud Photos started"

start-backup-from-icloud-photos-init-infra: ## Initialize infrastructure for iCloud Photos backup
	$(MAKE) drive-rabbitmq-new-queue
		

start-backup-from-icloud-photos-show-overview: ## Show overview of iCloud Photos backup
	./init.sh radmin show overview