"""Load and resolve ingestion configuration for the local Docker stack."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
import os
from typing import Final


REPO_ROOT: Final[Path] = Path(__file__).resolve().parents[4]
ENV_FILE: Final[Path] = REPO_ROOT / ".env"
DEFAULT_SOURCE_HOST: Final[str] = "postgres_source"
DEFAULT_SOURCE_PORT: Final[int] = 5432
DEFAULT_SOURCE_HOST_PORT: Final[int] = 5435
DEFAULT_SOURCE_DB: Final[str] = "football_source"
DEFAULT_SOURCE_USER: Final[str] = "football_source_user"
DEFAULT_SOURCE_PASSWORD: Final[str] = "change_me_source"
DEFAULT_COMPETITION_CODE: Final[str] = "E0"
DEFAULT_COMPETITION_NAME: Final[str] = "Premier League"
DEFAULT_START_YEAR: Final[int] = 1993


# Return the start year for the current football season.
def current_season_start_year(today: date | None = None) -> int:
    current_day = today or date.today()
    return current_day.year if current_day.month >= 7 else current_day.year - 1


@dataclass(frozen=True, slots=True)
class LoaderConfig:
    source_host: str
    source_port: int
    source_host_port: int
    source_db: str
    source_user: str
    source_password: str
    competition_code: str = DEFAULT_COMPETITION_CODE
    competition_name: str = DEFAULT_COMPETITION_NAME
    start_year: int = DEFAULT_START_YEAR
    end_year: int = current_season_start_year()
    source_base_url: str = "https://www.football-data.co.uk/mmz4281"
    env_file: Path = ENV_FILE


# Parse key-value pairs from a local .env-style file.
def parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")

    return values


# Resolve a setting using environment variables, file defaults, then a fallback.
def resolve_setting(name: str, defaults: dict[str, str], fallback: str) -> str:
    return os.environ.get(name) or defaults.get(name) or fallback


# Build the final loader configuration from environment and .env values.
def load_config(env_file: Path = ENV_FILE) -> LoaderConfig:
    defaults = parse_env_file(env_file)

    return LoaderConfig(
        source_host=resolve_setting("FDP_POSTGRES_SOURCE_HOST", defaults, DEFAULT_SOURCE_HOST),
        source_port=int(resolve_setting("FDP_POSTGRES_SOURCE_PORT", defaults, str(DEFAULT_SOURCE_PORT))),
        source_host_port=int(
            resolve_setting("FDP_POSTGRES_SOURCE_HOST_PORT", defaults, str(DEFAULT_SOURCE_HOST_PORT))
        ),
        source_db=resolve_setting("FDP_POSTGRES_SOURCE_DB", defaults, DEFAULT_SOURCE_DB),
        source_user=resolve_setting("FDP_POSTGRES_SOURCE_USER", defaults, DEFAULT_SOURCE_USER),
        source_password=resolve_setting("FDP_POSTGRES_SOURCE_PASSWORD", defaults, DEFAULT_SOURCE_PASSWORD),
        env_file=env_file,
    )
