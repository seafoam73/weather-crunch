CREATE TABLE dim_city (
    city_id INTEGER PRIMARY KEY,
    city_name VARCHAR,
    state VARCHAR,
    country VARCHAR,
    zip VARCHAR
);

CREATE TABLE dim_weather (
    weather_id INTEGER PRIMARY KEY,
    weather_name VARCHAR
);

CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY,
    full_datetime TIMESTAMP,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    hour INTEGER
);

CREATE TABLE fact_event (
    event_id INTEGER PRIMARY KEY,
    city_id INTEGER,
    weather_id INTEGER,
    date_id INTEGER,
    temperature INTEGER,
    pressure DECIMAL,
    humidity DECIMAL,
    wind_speed DECIMAL,
    FOREIGN KEY (city_id) REFERENCES dim_city(city_id),
    FOREIGN KEY (weather_id) REFERENCES dim_weather(weather_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);