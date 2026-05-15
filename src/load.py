import pandas as pd
from sqlalchemy import create_engine, insert, MetaData, Table, select
import os
from dotenv import load_dotenv
from transform import transform_weather
from extract import extract_weather

# Load environment variables from .env
load_dotenv()

#retreives DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

#uses SQLalchemy to translate between pandas and PostgreSQL. Sets up the instructions to connect to 1.reference the SQL dataset and 2.place the existing dataframes data into the correct tables
engine = create_engine(DATABASE_URL)

#Reflecting the tables to the function so it knows the PK and FKs are there
metadata = MetaData()
dim_city = Table("dim_city", metadata, autoload_with=engine)
dim_weather = Table("dim_weather", metadata, autoload_with=engine)
dim_date = Table("dim_date", metadata, autoload_with=engine)
fact_event = Table("fact_event", metadata, autoload_with=engine)

#calls the ET data and puts the dataframe into each SQL tables
def weather_load():
    data_A, data_B = extract_weather()
    df = transform_weather(data_A, data_B)
    with engine.connect() as conn:
        existing_city = conn.execute(select(dim_city).where(dim_city.c.city_name == df["city_name"].iloc[0])).fetchone()
        if existing_city:
            city_id = existing_city.city_id
        else:
            result = conn.execute(insert(dim_city).values(
            city_name=df["city_name"].iloc[0],
            state=df["state"].iloc[0],
            country=df["country"].iloc[0]
            ))
            city_id = result.inserted_primary_key[0]
        conn.commit()
        existing_weather = conn.execute(select(dim_weather).where(dim_weather.c.weather_name == df["weather_name"].iloc[0])).fetchone()
        if existing_weather:
            weather_id = existing_weather.weather_id
        else:
            result = conn.execute(insert(dim_weather).values(weather_name=df["weather_name"].iloc[0]))
            weather_id = result.inserted_primary_key[0]
        conn.commit()
        result = conn.execute(insert(dim_date).values(
            full_datetime=df["full_datetime"].iloc[0],
            year=int(df["year"].iloc[0]),
            month=int(df["month"].iloc[0]),
            day=int(df["day"].iloc[0]),
            hour=int(df["hour"].iloc[0])
            ))
        date_id = result.inserted_primary_key[0]
        conn.commit()
        result = conn.execute(insert(fact_event).values(
            city_id=city_id,
            weather_id=weather_id,
            date_id=date_id,
            temperature=int(df["temperature"].iloc[0]),
            pressure=float(df["pressure"].iloc[0]),
            humidity=float(df["humidity"].iloc[0]),
            wind_speed=float(df["wind_speed"].iloc[0])
            ))
        event_id = result.inserted_primary_key[0]
        conn.commit()

if __name__ == "__main__":
    weather_load()
    print("Data loaded successfully!")

