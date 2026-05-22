import pandas as pd
from sqlalchemy import create_engine, insert, MetaData, Table, select
import os
from dotenv import load_dotenv
from transform import transform_weather, iterate_weather
from extract import url_feed, lat_lon, extract_weather, missouri_prime

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

url_a = url_feed(missouri_prime)
url_b = lat_lon(url_feed(missouri_prime))

#calls the ET data as a 5 row DataFrame, iterates through each row and puts the data from that row into each corresponding SQL tables.
def weather_load():
    data_geo, data_weather = extract_weather(url_a, url_b)
    df = iterate_weather(data_geo, data_weather)
    for index, row in df.iterrows():
        with engine.connect() as conn:
            existing_city = conn.execute(select(dim_city).where(dim_city.c.city_name == row["city_name"])).fetchone()
            if existing_city:
                city_id = existing_city.city_id
            else:
                result = conn.execute(insert(dim_city).values(
                city_name=row["city_name"],
                state=row["state"],
                country=row["country"]
                ))
                city_id = result.inserted_primary_key[0]
            conn.commit()
            existing_weather = conn.execute(select(dim_weather).where(dim_weather.c.weather_name == row["weather_name"])).fetchone()
            if existing_weather:
                weather_id = existing_weather.weather_id
            else:
                result = conn.execute(insert(dim_weather).values(weather_name=row["weather_name"]))
                weather_id = result.inserted_primary_key[0]
            conn.commit()
            result = conn.execute(insert(dim_date).values(
                full_datetime=row["full_datetime"],
                year=int(row["year"]),
                month=int(row["month"]),
                day=int(row["day"]),
                hour=int(row["hour"])
                ))
            date_id = result.inserted_primary_key[0]
            conn.commit()
            result = conn.execute(insert(fact_event).values(
                city_id=city_id,
                weather_id=weather_id,
                date_id=date_id,
                temperature=int(row["temperature"]),
                pressure=float(row["pressure"]),
                humidity=float(row["humidity"]),
                wind_speed=float(row["wind_speed"])
                ))
            event_id = result.inserted_primary_key[0]
            conn.commit()

if __name__ == "__main__":
    weather_load()
    print("Data loaded successfully!")


