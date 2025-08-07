start-budo-backup-info:
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

# -b google_photos
start-budo-backup: ## Start backup from iCloud Photos
	@echo "Starting backup from iCloud Photos"		
	$(PYTHON) -m src.entry.functions.start_budo_backup 
	@echo "Backup from iCloud Photos started"
