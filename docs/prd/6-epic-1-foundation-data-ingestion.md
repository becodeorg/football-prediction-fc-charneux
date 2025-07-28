# 6. Epic 1: Foundation & Data Ingestion

**Expanded Goal:** This epic aims to establish the fundamental data infrastructure for the Football Match Prediction system. This includes setting up the SQLite database, loading the initial historical match data from the provided CSV, and implementing a basic web scraping mechanism to collect real-time betting odds. The successful completion of this epic will provide a robust and continuously updated data foundation for subsequent model training and prediction.

## 6.1. Story 1.1: Database Setup and Historical Data Ingestion

As a **Data Engineer**,
I want to **set up the SQLite database and ingest historical match data**,
so that **the system has a foundational dataset for model training and analysis.**

### Acceptance Criteria

1.  **1**: The `football.db` SQLite database is created.
2.  **2**: A `matches` table is created within `football.db` with a schema capable of storing all relevant columns from the historical CSV data (Date, Time, HomeTeam, AwayTeam, FTHG, FTAG, FTR, and additional statistics/odds).
3.  **3**: The provided `historical_data.csv` (or equivalent) is successfully loaded into the `matches` table.
4.  **4**: The `db_setup.py` script is executable and idempotent (can be run multiple times without error, replacing existing data if necessary).
5.  **5**: A `.gitignore` entry is added to exclude `football.db` from version control.

## 6.2. Story 1.2: Basic Betting Odds Scraper

As a **Data Engineer**,
I want to **implement a basic web scraper for betting odds**,
so that **the system can collect real-time odds data for upcoming matches.**

### Acceptance Criteria

1.  **1**: The `scraper.py` script is capable of making HTTP requests to the specified betting odds websites (e.g., WhoScored, SportsGambler, OddsChecker, BetFirst).
2.  **2**: The scraper can extract relevant betting odds (e.g., Home Win, Draw, Away Win odds) for upcoming matches.
3.  **3**: The extracted odds data is structured and can be stored in the `football.db` database, potentially in a new table or by updating existing match records.
4.  **4**: The `scraper.py` script includes basic error handling for network issues or changes in website structure.
5.  **5**: The `scraper.py` script is executable independently for testing purposes.
