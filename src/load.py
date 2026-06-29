import pandas as pd
from sqlalchemy import create_engine, insert, MetaData, Table, select
import os
from transform import transform_weather, iterate_weather
from extract import url_feed, lat_lon, extract_weather, missouri_prime
#The following two lines are only necessary when the .env variables are not run externally i.e. Github. Used when ran locally
#from dotenv import load_dotenv
#load_dotenv()

#calls the Extract/Transform data as a 5 row DataFrame, iterates through each row and puts the data from that row into the corresponding SQL tables.
def weather_load():
    #retrieves DATABASE_URL from .env or github depending on whether it is run locally or github
    DATABASE_URL = os.getenv("DATABASE_URL")

    #uses SQLalchemy to translate between pandas and PostgreSQL. Sets up the instructions to connect to 1.reference the SQL dataset and 2.place the existing dataframes data into the correct tables
    engine = create_engine(DATABASE_URL)

    #Reflecting the tables to the function so it knows the PK and FKs are there
    metadata = MetaData()
    dim_city = Table("dim_city", metadata, autoload_with=engine)
    dim_weather = Table("dim_weather", metadata, autoload_with=engine)
    dim_date = Table("dim_date", metadata, autoload_with=engine)
    fact_event = Table("fact_event", metadata, autoload_with=engine)

    #calls the extract.py functions to extract the weather data
    url_a = url_feed(missouri_prime)
    url_b = lat_lon(url_a)
    data_geo, data_weather = extract_weather(url_a, url_b)
    #calls the transform.py function to prepare the data for loading
    df = iterate_weather(data_geo, data_weather)
    #iterates through each row of the DataFrame and connects to the postgresql database
    for index, row in df.iterrows():
        with engine.connect() as conn:
            #Checks to see if the "city_name" is already in the table if not it adds the city with paired data values to the dim_city table. Otherwise, the city is skipped.
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
            #Checks to see if the "weather_name" is already in the table if not it loads the weather condition to the dim_weather table. Otherwise, the weather condition is skipped.
            existing_weather = conn.execute(select(dim_weather).where(dim_weather.c.weather_name == row["weather_name"])).fetchone()
            if existing_weather:
                weather_id = existing_weather.weather_id
            else:
                result = conn.execute(insert(dim_weather).values(weather_name=row["weather_name"]))
                weather_id = result.inserted_primary_key[0]
            conn.commit()
            #Loads the new date values into the dim_date table
            result = conn.execute(insert(dim_date).values(
                full_datetime=row["full_datetime"],
                year=int(row["year"]),
                month=int(row["month"]),
                day=int(row["day"]),
                hour=int(row["hour"])
                ))
            date_id = result.inserted_primary_key[0]
            conn.commit()
            #Loads the new fact event into the fact_event table
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

#calls the function with the variables below only when the file itself is ran. As opposed to being imported as intended
if __name__ == "__main__":
    weather_load()
    print("Data loaded successfully!")


