generate-features: ## generate features
	@echo "Generating features for ${PWD}"
	@read -p "Enter feature name: " feature_name; \
	uv run generate/feature/folders.py -b ${PWD} -f $$feature_name
	uv run generate/feature/tasks.py -b ${PWD} -f $$feature_name
