"""Run the ingestion job that downloads and stores Premier League seasons."""

from __future__ import annotations

from .config import load_config
from .db import connect_to_source, ensure_schema_and_table, load_frame
from .football_data import annotate_frame, build_competition_url, download_competition_season


# Ingest all configured seasons into the SOURCE database.
def ingest_seasons(start_year: int | None = None, end_year: int | None = None) -> int:
    config = load_config()
    first_year = start_year or config.start_year
    last_year = end_year or config.end_year
    total_rows = 0

    with connect_to_source(config) as connection:
        ensure_schema_and_table(connection)

        for year in range(first_year, last_year + 1):
            source_url = build_competition_url(config.source_base_url, year, config.competition_code)
            frame = download_competition_season(source_url)
            annotated = annotate_frame(frame, config, year, source_url)
            total_rows += load_frame(
                connection,
                annotated,
                competition_name=config.competition_name,
                competition_code=config.competition_code,
                season_label=f"{year}/{year + 1}",
                season_code=f"{year % 100:02d}{(year + 1) % 100:02d}",
                source_url=source_url,
            )

    return total_rows


# Run the ingestion job and print the total loaded rows.
def main() -> int:
    rows = ingest_seasons()
    print(f"Loaded {rows} rows into football_source.raw_matches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
