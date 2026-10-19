"""Download and annotate Football-Data.co.uk season CSV files."""

from __future__ import annotations

from io import StringIO

import pandas as pd
import requests

from .config import LoaderConfig


# Convert a season start year into the Football-Data.co.uk code.
def season_code(start_year: int) -> str:
    return f"{start_year % 100:02d}{(start_year + 1) % 100:02d}"


# Format a season label in the standard human-readable form.
def season_label(start_year: int) -> str:
    return f"{start_year}/{start_year + 1}"


# Build the download URL for one competition season CSV.
def build_competition_url(base_url: str, start_year: int, competition_code: str) -> str:
    return f"{base_url}/{season_code(start_year)}/{competition_code}.csv"


# Download a CSV season file and load it into a DataFrame.
def download_competition_season(url: str, timeout_seconds: int = 30) -> pd.DataFrame:
    response = requests.get(url, timeout=timeout_seconds)
    response.raise_for_status()
    return pd.read_csv(StringIO(response.text), engine="python", on_bad_lines="skip")   
    


# Add ingestion metadata columns to the raw match DataFrame.
def annotate_frame(frame: pd.DataFrame, config: LoaderConfig, start_year: int, source_url: str) -> pd.DataFrame:
    annotated = frame.copy()
    annotated.insert(0, "competition_name", config.competition_name)
    annotated.insert(1, "competition_code", config.competition_code)
    annotated.insert(2, "season_label", season_label(start_year))
    annotated.insert(3, "season_code", season_code(start_year))
    annotated.insert(4, "source_url", source_url)
    annotated.insert(5, "source_row_number", range(1, len(annotated) + 1))
    return annotated
