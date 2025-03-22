PYTHON=(uv run python)


help: ## this help
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?##"} /^[a-zA-Z_-]+:.*?## / { printf "\t\033[36m%-20s\033[0m\t%s\n", $$1, $$2 }' $(MAKEFILE_LIST) | sort

install: ## install project dependencies
	uv install

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