PYTHON=uv run python
TARGET_ORIGIN= ./target/origin
TARGET_SOURCE= ./target/source

.PHONY: help install check-version generate-features coverage coverage-unitary test lint install-requirements install-requirements-ci scan-complexity clean start-backup-from-icloud-photos sync-repository start-repository


help: ## this help
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?##"} /^[a-zA-Z_-]+:.*?## / { printf "\t\033[36m%-20s\033[0m\t%s\n", $$1, $$2 }' $(MAKEFILE_LIST) | sort

install: ## install project dependencies
	uv install

check-version: ## check the version of the uv python environment
	@echo "Checking uv version"
	@uv --version
	@$(PYTHON) --version

generate-features: ## generate features
	@echo "Generating features for ${PWD}"
	@read -p "Enter feature name: " feature_name; \
	uv run generate/feature/folders.py -b ${PWD} -f $$feature_name
	uv run generate/feature/tasks.py -b ${PWD} -f $$feature_name

coverage: ## This will run the tests and generate a coverage report
	$(PYTHON) -m pytest -v --cov-report term-missing --cov=src/ --cov-report=xml --disable-warnings

coverage-unitary: ## This will run the tests for unitary tests and generate a coverage report
	$(PYTHON) -m pytest tests/unitary -v \
		--cov-report term-missing \
		--cov=src/ \
		--cov-report=xml \
		--disable-warnings \
		--cov-branch

test: ## This will run the tests
	$(PYTHON) -m pytest

lint: ## This will run the linter
	$(PYTHON) -m bandit src/ -r
	$(PYTHON) -m black src/
	$(PYTHON) -m black tests/

install-requirements: ## This will install the requirements
	uv sync

install-requirements-ci: ## This will install the requirements for CI
	pip install poetry
	uv install --no-root 


scan-complexity: ## This will run the complexity scanner
	radon cc source/ -a

clean: ## Remove cache files
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name ".pytest_cache" -type d | xargs rm -rf

start-backup-from-icloud-photos: ## Start backup from iCloud Photos
	@echo "Starting backup from iCloud Photos"
	uv run src/entry/functions/backup_from_icloud_photos/workflow.py \
		--origin ./target/origin \
		--destination ./target/destination \
		--log-level info
	@echo "Backup from iCloud Photos started"

sync-repository: ## Sync the repository
	@echo "Syncing repository"
	git fetch --all
	git reset --hard origin/main
	git pull origin main
	@echo "Repository synced"

start-repository: ## Start the repository
	@echo "Starting repository"
	uv run src/entry/functions/start_repository/workflow.py \
		--origin $(TARGET_ORIGIN) \
		--destination ./target/destination \
		--log-level info
	@echo "Repository started"

show_origin: ## Show the origin target path
	@echo "Origin target path: $(TARGET_ORIGIN)"
show_source: ## Show the source target path
	@echo "Source target path: $(TARGET_SOURCE)"