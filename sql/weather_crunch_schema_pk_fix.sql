DROP TABLE fact_event;
DROP TABLE dim_city;
DROP TABLE dim_weather;
DROP TABLE dim_date;

CREATE TABLE dim_city (
    city_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    city_name VARCHAR,
    state VARCHAR,
    country VARCHAR
);

CREATE TABLE dim_weather (
    weather_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    weather_name VARCHAR
);

CREATE TABLE dim_date (
    date_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    full_datetime TIMESTAMP,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    hour INTEGER
);

CREATE TABLE fact_event (
    event_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
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