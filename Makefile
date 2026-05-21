.PHONY: help install dev test lint format run seed docker-up docker-down clean

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	pip install -r requirements.txt

dev: ## Install all dependencies (production + development)
	pip install -r requirements.txt -r requirements-dev.txt

test: ## Run tests with pytest
	pytest tests/ -v --tb=short

test-cov: ## Run tests with coverage report
	pytest tests/ --cov=app --cov-report=html --cov-report=term-missing

lint: ## Run linter (ruff)
	ruff check app/ tests/

format: ## Format code with ruff
	ruff check --fix app/ tests/
	ruff format app/ tests/

run: ## Run the development server
	flask run --debug --port 5000

seed: ## Seed the database with sample data
	python build_database.py

migrate: ## Run database migrations
	flask db upgrade

migrate-create: ## Create a new migration (usage: make migrate-create MSG="description")
	flask db migrate -m "$(MSG)"

docker-up: ## Start the application with Docker
	docker compose up --build -d

docker-down: ## Stop Docker containers
	docker compose down

clean: ## Remove cached files and build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache htmlcov .coverage .mypy_cache dist build *.egg-info

