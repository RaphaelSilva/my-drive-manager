include .env
-include !generate/Makefile
-include !src/entry/functions/*/Makefile
-include !src/feature/backup_photos_from/infrastructure/drivers/rabbitmq/Makefile

# Makefile for managing the project
PYTHON=uv run python
TARGET_ORIGIN ?= ./target/origin
TARGET_DESTINATION ?= ./target/destination



help: ## this help
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?##"} /^[a-zA-Z_-]+:.*?## / { printf "\t\033[36m%-20s\033[0m\t%s\n", $$1, $$2 }' $(MAKEFILE_LIST) | sort	

check-env: ## check the environment variables
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


install: ## install project dependencies
	uv install

check-version: ## check the version of the uv python environment
	@echo "Checking uv version"
	@uv --version
	@$(PYTHON) --version

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

scan-complexity: ## This will run the complexity scanner
	radon cc source/ -a

clean: ## Remove cache files
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name ".pytest_cache" -type d | xargs rm -rf

sync-repository: ## Sync the repository
	@echo "Syncing repository"
	git fetch --all
	git reset --hard origin/main
	git pull origin main
	@echo "Repository synced"

run_sanity: ## Run the sanity checks
	@echo "Running sanity checks"
	$(PYTHON) -m src.feature.backup_photos_from.infrastructure.drivers.rabbitmq \
		--run sanity_check \

container-down: ## Stop local development services
	@echo "Stopping local development services"
	docker compose -f ./docker-compose.yml down

container-up: ## Start container services
	@echo "Starting container services $(RABBITMQ_CONTAINER_NAME)"
	@echo "If it didn't work, try running 'make image-services-build' manually"
	docker compose -f ./docker-compose.yml up -d
	
image-services-build: ## Build container services
	@echo "Building container services"
	for f in $(wildcard ./dockerfile/*/Makefile); do \
		make -f $$f build; \
	done