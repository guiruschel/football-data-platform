# Football Data Platform

End-to-end Data Engineering platform using public football data from the Premier League.

## Overview

This project demonstrates modern Data Engineering practices using open-source tools running locally via Docker. The ingestion layer, its dependencies, and its tests run inside containers:

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


### Local Postgres ports

- `postgres_source` inside Docker uses port `5432`
- the host-side mapping for DBeaver is `5435`
- `postgres_dw` uses host port `5434`

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

## BI Focus Areas

The first analytical views planned for Metabase are:

1. **Team performance**
        - wins, draws, losses
        - goals scored and conceded
        - goal difference
        - points by season
        - ranking over time

2. **Recent form and consistency**
        - last 5 or 10 matches by team
        - winning and losing streaks
        - unbeaten runs

3. **Season-to-season comparison**
        - team performance changes over the years
        - teams that improved or declined in level
        - evolution of home wins, draws, and losses
        - comparison of points and goal difference across seasons

## Quick Start

> Prerequisites: Docker Desktop, Git

```bash
# Clone the repository
git clone git@github.com:<your-username>/football-data-platform.git
cd football-data-platform

# Copy environment variables template
cp .env.example .env
# Edit .env with your values

# Start the local stack
make up

# Run the ingestion tests inside Docker
docker compose run --rm ingestion python -m pytest ingestion/tests -q

# Run the loader inside Docker
docker compose run --rm ingestion python -m football_data_platform.cli
```

The project does not require Python installed on the Windows host for the ingestion step; the Docker image provides the runtime and packages.

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
