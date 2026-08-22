# Football Data Platform

End-to-end Data Engineering platform using public football data from the Premier League.

## Overview

This project demonstrates modern Data Engineering practices using open-source tools running locally via Docker:

- **Ingestion:** Airbyte (PostgreSQL SOURCE → PostgreSQL DW)
- **Transformation:** dbt (staging → intermediate → marts)
- **Orchestration:** Apache Airflow
- **Data Quality:** dbt tests + Great Expectations
- **BI:** Metabase
- **IaC:** Terraform
- **CI/CD:** GitHub Actions
- **Lineage:** OpenLineage + Marquez
- **Security:** Trivy + secret scanning

## Dataset

- **Source:** [Football-Data.co.uk](https://www.football-data.co.uk/)
- **Competition:** Premier League
- **Period:** 1993 → present
- **Format:** CSV
- **Grain:** one row per match

## Architecture

```text
Football-Data.co.uk
        ↓
Python Dataset Loader
        ↓
PostgreSQL SOURCE
        ↓
Airbyte
        ↓
PostgreSQL DW / RAW
        ↓
dbt (staging → intermediate → marts)
        ↓
Metabase
```

Orchestrated by **Airflow**. Validated by **dbt tests** and **Great Expectations**.

## Quick Start

> Prerequisites: Docker Desktop, Python 3.11+, Git

```bash
# Clone the repository
git clone git@github.com:<your-username>/football-data-platform.git
cd football-data-platform

# Copy environment variables template
cp .env.example .env
# Edit .env with your values

# Start all services
make up

# Run the full pipeline
make pipeline
```

## Project Structure

```text
football-data-platform/
├── .github/workflows/     # CI/CD pipelines
├── airflow/dags/          # Airflow DAGs
├── airbyte/connections/   # Airbyte connection configs
├── dbt/                   # dbt project (models, tests, macros)
├── ingestion/             # Python dataset loader
├── data_quality/          # Great Expectations expectations
├── terraform/             # Infrastructure as Code
├── docker/                # Dockerfiles
├── docs/                  # Project documentation
├── docker-compose.yml
├── Makefile
└── pyproject.toml
```

## Documentation

- [Project Context](docs/football_data_engineering_e2e_project_context.md) — Architecture, stack, and decisions
- [Progress](docs/project_progress.md) — Current status and roadmap
- [Checklist](docs/checklist.md) — Environment setup checklist

## Makefile Commands

```bash
make up          # Start all Docker services
make down        # Stop all Docker services
make pipeline    # Run the full data pipeline
make dbt-run     # Run dbt models
make dbt-test    # Run dbt tests
make lint        # Run all linters (Ruff + SQLFluff)
make test        # Run Pytest
make pre-commit  # Run pre-commit hooks
```

## License

MIT
