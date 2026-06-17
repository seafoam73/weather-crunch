# weather_crunch

A full-stack data engineering portfolio project that pulls live weather data for 5 
Missouri cities, transforms it into a normalized star schema, and loads it into a 
cloud PostgreSQL database on an automated schedule.

## What It Does

A Python ETL pipeline runs 4x daily via GitHub Actions, pulling current weather 
conditions from the OpenWeatherMap API for Columbia, Kansas City, Jefferson City, 
Springfield, and St. Louis. Data is transformed and loaded into Supabase (PostgreSQL).

## Project Structure
weather_crunch/

├── src/

│   ├── extract.py        # Calls OpenWeatherMap Geo + Weather APIs for 5 MO cities

│   ├── transform.py      # Shapes API responses into a normalized DataFrame

│   └── load.py           # Loads transformed data into Supabase PostgreSQL

├── Spreadsheets/

│   └── weather_crunch_lat_lon.xlsx   # Lat/lon coordinates (sourced via Geo API)

├── .github/workflows/    # GitHub Actions cron schedule (4x daily, UTC)

└── weather_schema_v1.dbml  # Star schema design (dbdiagram.io)

## Data Model

Star schema with one fact table and three dimension tables:

- **`fact_event`** — weather observations loaded by the ETL pipeline
- **`dim_city`** — city reference data (Kansas City, Columbia, Jefferson City, Springfield, St. Louis)
- **`dim_weather`** — weather condition descriptions
- **`dim_date`** — calendar date and time breakdown

See `weather_schema_v1.dbml` for full schema definition.

## Pipeline

| Step | Tool | Details |
|------|------|---------|
| Extract | Python / OpenWeatherMap API | Geo API → coordinates; Weather API → conditions |
| Transform | Python / pandas | Normalizes JSON responses into a star-schema DataFrame |
| Load | Python / psycopg2 | Inserts into Supabase via Transaction pooler |
| Schedule | GitHub Actions | Cron: 13:00, 18:00, 00:00, 06:00 UTC (7am/12pm/7pm/12am CDT) |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python (pandas, requests, SQLAlchemy) |
| API | OpenWeatherMap (Geo + Weather endpoints) |
| Database | Supabase PostgreSQL (Transaction pooler) |
| Scheduling | GitHub Actions |
| Version Control | Git / GitHub |

## Setup

1. Clone the repo
2. Add the following GitHub secret: `WEATHER_KEY` (OpenWeatherMap API key)
3. The workflow maps `WEATHER_KEY` → `API_KEY` in the env block
4. GitHub Actions will run the pipeline automatically per the cron schedule

> **Note:** Supabase free tier requires the Transaction connection pooler 
> (`aws-1-us-east-2.pooler.supabase.com:6543`). Direct connections will fail 
> due to IPv6 restrictions.