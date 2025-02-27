
help: ## this help
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?##"} /^[a-zA-Z_-]+:.*?## / { printf "\t\033[36m%-20s\033[0m\t%s\n", $$1, $$2 }' $(MAKEFILE_LIST) | sort

install: ## install project dependencies
	poetry install

generate-features: ## generate features
	@echo "Generating features for ${PWD}"
	@read -p "Enter feature name: " feature_name; \
	uv run generate/feature/folders.py -b ${PWD} -f $$feature_name

