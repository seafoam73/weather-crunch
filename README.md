# weather_crunch

A full-stack data engineering and analytics portfolio project that pulls live weather data 
for 5 Missouri cities, transforms it into a star schema, and loads it into a cloud 
PostgreSQL database on an automated schedule. The data is then combined with a forecast 
API and geographic reference data in a Power BI semantic model, delivering interactive 
dashboards that visualize past, current, and forecasted weather conditions.

## What It Does

A Python ETL pipeline runs 4x daily via GitHub Actions, pulling current weather conditions 
from the OpenWeatherMap API for Columbia, Kansas City, Jefferson City, Springfield, and 
St. Louis. Data is transformed and loaded into Supabase (PostgreSQL). From there, the 
pipeline data is combined with Open-Meteo forecast data and geographic reference data in 
Power BI, where it is shaped into a constellation schema semantic model and visualized 
across four dashboard pages covering current conditions, 21-day history, city-level deep 
dive, and tomorrow's forecast.

## Project Structure

```
weather_crunch/

├── src/
│   ├── extract.py        # Calls OpenWeatherMap Geo + Weather APIs for 5 MO cities
│   ├── transform.py      # Shapes API responses into a normalized DataFrame
│   └── load.py           # Loads transformed data into Supabase PostgreSQL

├── Spreadsheets/
│   └── weather_crunch_lat_lon.xlsx   # Lat/lon coordinates (sourced via Geo API)

├── sql/
│   └── full_fact_event_view.sql      # Supabase views for data governance

├── dashboard/
│   └── weather_crunch.pbix           # Power BI constellation schema semantic model and 4-page dashboard

├── .github/workflows/    # GitHub Actions cron schedule (4x daily, UTC)
└── weather_schema_v1.dbml  # Star schema design (dbdiagram.io)
```

## Data Model

### Weather_Crunch_Cloud Model
Star schema with one fact table and three dimension tables:

- **`fact_event`** — weather observations loaded by the ETL pipeline
- **`dim_city`** — city reference data (Kansas City, Columbia, Jefferson City, Springfield, St. Louis)
- **`dim_weather`** — weather condition descriptions
- **`dim_date`** — calendar date and time breakdown

See `weather_schema_v1.dbml` for full schema definition.

### Power BI Semantic Model

Constellation schema built on three data sources: Supabase (pipeline data), Open-Meteo API (forecast data), and a geographic reference spreadsheet. It contains two fact tables sharing a common dimension:

- **`fact_event`** — historical weather observations loaded by the ETL pipeline
- **`fact_forecast`** — rolling 48-hour forecast data pulled via M Query from Open-Meteo
- **`dim_city`** — shared dimension connecting both fact tables
- **`lat_lon`** — geographic reference table supporting map visuals for dim_city
- **`weather_code_phrase`** — maps Open-Meteo WMO weather codes to descriptions

## Pipeline

| Step | Tool | Details |
|------|------|---------|
| Extract | Python / OpenWeatherMap API | Geo API → coordinates; Weather API → conditions |
| Transform | Python / pandas | Normalizes JSON responses into a star-schema DataFrame |
| Load | Python / Sqlalchemy | Inserts into Supabase via Transaction pooler |
| Schedule | GitHub Actions | Cron: 13:00, 18:00, 00:00, 06:00 UTC (7am/12pm/7pm/12am CDT) |
| Import | Power Query / M | Loads Supabase data, Open-Meteo API, and lat/lon spreadsheet into the semantic model |
| Visualize | Power BI / DAX | 4-page dashboard covering current conditions, 21-day history, city deep dive, and tomorrow's forecast |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python (pandas, requests, SQLAlchemy) |
| API | OpenWeatherMap (Geo + Weather endpoints), Open-Meteo (forecast data) |
| Database | Supabase PostgreSQL (Transaction pooler) |
| Scheduling | GitHub Actions |
| Reference Data | Excel (lat/lon coordinate spreadsheet) |
| BI / Visualization | Power BI Desktop (Power Query / M, DAX) |
| Version Control | Git / GitHub |

## Setup

1. Clone the repo
2. Add the following GitHub secrets: `WEATHER_KEY` (OpenWeatherMap API key) and `DATABASE_URL` (Supabase Transaction pooler connection string)
3. The workflow maps `WEATHER_KEY` → `API_KEY` in the env block
4. GitHub Actions will run the pipeline automatically per the cron schedule
5. Open `dashboard/weather_crunch.pbix` in Power BI Desktop to view the dashboard. The file connects to Supabase via the Transaction pooler — update the connection credentials if running against your own Supabase instance.

> **Note:** Supabase free tier requires the Transaction connection pooler 
> (`aws-1-us-east-2.pooler.supabase.com:6543`). Direct connections will fail 
> due to IPv6 restrictions.
