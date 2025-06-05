start-backup-from-icloud-photos: ## Start backup from iCloud Photos
	@echo "Starting backup from iCloud Photos"
	$(PYTHON) src/entry/functions/backup_from_icloud_photos/workflow.py \
		--origin $(TARGET_ORIGIN) \
		--destination $(TARGET_DESTINATION) \
		--log-level info
	@echo "Backup from iCloud Photos started"