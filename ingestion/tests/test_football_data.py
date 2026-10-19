"""Test the pure helper functions that support the ingestion loader."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pandas as pd

from football_data_platform.config import LoaderConfig, parse_env_file
from football_data_platform.db import row_to_payload
from football_data_platform.football_data import (
    annotate_frame,
    build_competition_url,
    download_competition_season,
    season_code,
    season_label,
)


# Check season code formatting for known years.
def test_season_code() -> None:
    assert season_code(1993) == "9394"
    assert season_code(2025) == "2526"


# Check season label formatting for known years.
def test_season_label() -> None:
    assert season_label(1993) == "1993/1994"


# Check the Football-Data.co.uk URL builder.
def test_build_competition_url() -> None:
    assert build_competition_url("https://www.football-data.co.uk/mmz4281", 2023, "E0") == (
        "https://www.football-data.co.uk/mmz4281/2324/E0.csv"
    )


# Check that .env-style files are parsed correctly.
def test_parse_env_file(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        """
        FDP_POSTGRES_SOURCE_HOST=localhost
        FDP_POSTGRES_SOURCE_PORT=5433
        FDP_POSTGRES_SOURCE_HOST_PORT=5435
        FDP_POSTGRES_SOURCE_DB=football_source
        FDP_POSTGRES_SOURCE_USER=football_source_user
        FDP_POSTGRES_SOURCE_PASSWORD=secret
        """.strip(),
        encoding="utf-8",
    )

    values = parse_env_file(env_file)
    assert values["FDP_POSTGRES_SOURCE_DB"] == "football_source"


# Check that ingestion metadata columns are added in the expected order.
def test_annotate_frame() -> None:
    config = LoaderConfig(
        source_host="localhost",
        source_port=5433,
        source_host_port=5435,
        source_db="football_source",
        source_user="football_source_user",
        source_password="secret",
    )
    frame = pd.DataFrame([{"Date": "01/08/2025", "HomeTeam": "Arsenal", "AwayTeam": "Chelsea"}])

    annotated = annotate_frame(frame, config, 2025, "https://example.test/E0.csv")

    assert list(annotated.columns[:6]) == [
        "competition_name",
        "competition_code",
        "season_label",
        "season_code",
        "source_url",
        "source_row_number",
    ]
    assert annotated.iloc[0]["competition_code"] == "E0"
    assert annotated.iloc[0]["season_code"] == "2526"


# Check that missing values are converted into JSON-safe nulls.
def test_row_to_payload() -> None:
    row = pd.Series({"Date": "01/08/2025", "Unnamed: 7": float("nan"), "FTHG": 2})

    payload = row_to_payload(row)

    assert payload["Date"] == "01/08/2025"
    assert payload["Unnamed: 7"] is None
    assert payload["FTHG"] == 2


# Check that malformed CSV rows are skipped when downloading a season file.
def test_download_competition_season_skips_bad_lines(monkeypatch) -> None:
    csv_text = """Date,HomeTeam,AwayTeam
01/08/2025,Arsenal,Chelsea
02/08/2025,Man City,Liverpool,extra,values
03/08/2025,Spurs,Everton
"""

    def fake_get(url: str, timeout: int):
        assert url == "https://example.test/E0.csv"
        assert timeout == 30
        return SimpleNamespace(text=csv_text, raise_for_status=lambda: None)

    monkeypatch.setattr("football_data_platform.football_data.requests.get", fake_get)

    frame = download_competition_season("https://example.test/E0.csv")

    assert len(frame) == 2
    assert list(frame["HomeTeam"]) == ["Arsenal", "Spurs"]
