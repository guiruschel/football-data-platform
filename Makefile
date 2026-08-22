.PHONY: help up down restart logs pipeline \
        dbt-run dbt-test dbt-build dbt-compile dbt-docs \
        lint lint-python lint-sql \
        test test-cov \
        pre-commit \
        tf-fmt tf-validate tf-plan \
        clean

# Default target
help:
	@echo ""
	@echo "Football Data Platform — available commands"
	@echo ""
	@echo "  make up            Start all Docker services"
	@echo "  make down          Stop all Docker services"
	@echo "  make restart       Restart all Docker services"
	@echo "  make logs          Tail Docker logs"
	@echo ""
	@echo "  make pipeline      Run the full data pipeline"
	@echo ""
	@echo "  make dbt-run       Run dbt models"
	@echo "  make dbt-test      Run dbt tests"
	@echo "  make dbt-build     Run dbt build (models + tests)"
	@echo "  make dbt-compile   Compile dbt project"
	@echo "  make dbt-docs      Generate and serve dbt docs"
	@echo ""
	@echo "  make lint          Run all linters"
	@echo "  make lint-python   Run Ruff"
	@echo "  make lint-sql      Run SQLFluff"
	@echo ""
	@echo "  make test          Run Pytest"
	@echo "  make test-cov      Run Pytest with coverage"
	@echo ""
	@echo "  make pre-commit    Run pre-commit hooks on all files"
	@echo ""
	@echo "  make tf-fmt        Terraform fmt"
	@echo "  make tf-validate   Terraform validate"
	@echo "  make tf-plan       Terraform plan"
	@echo ""
	@echo "  make clean         Remove generated files"
	@echo ""

# Docker
up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

# Pipeline
pipeline:
	@echo "Running full pipeline..."
	@echo "Step 1: Airbyte sync (manual or via Airflow)"
	@echo "Step 2: dbt build"
	$(MAKE) dbt-build

# dbt
dbt-run:
	cd dbt && dbt run

dbt-test:
	cd dbt && dbt test

dbt-build:
	cd dbt && dbt build

dbt-compile:
	cd dbt && dbt compile

dbt-docs:
	cd dbt && dbt docs generate && dbt docs serve

# Lint
lint: lint-python lint-sql

lint-python:
	ruff check .
	ruff format --check .

lint-sql:
	sqlfluff lint dbt/models

# Tests
test:
	pytest

test-cov:
	pytest --cov --cov-report=term-missing

# pre-commit
pre-commit:
	pre-commit run --all-files

# Terraform
tf-fmt:
	terraform -chdir=terraform fmt -recursive -check

tf-validate:
	terraform -chdir=terraform validate

tf-plan:
	terraform -chdir=terraform plan

# Clean
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf dbt/target dbt/dbt_packages dbt/logs
