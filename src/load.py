import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from transform import transform_weather
from extract import extract_weather

# Load environment variables from .env
load_dotenv()

#retreives DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

#uses SQLalchemy to translate between pandas and PostgreSQL. Sets up the instructions to connect to to_sql()
engine = create_engine(DATABASE_URL)

#calls the transform.py transformed data and puts the datafram into each SQL tables
def weather_load():
    data_A, data_B = extract_weather()
    df = transform_weather(data_A, data_B)
    city_columns = df[["city_name", "state", "country"]]
    weather_column = df[["weather_name"]]
    date_column = df[["full_datetime", "year", "month", "day", "hour"]]
    fact_column = df[["temperature", "pressure", "humidity", "wind_speed"]]
    city_columns.to_sql(name="dim_city", con=engine, if_exists='append', index=False)
    weather_column.to_sql(name="dim_weather", con=engine, if_exists='append', index=False)
    date_column.to_sql(name="dim_date", con=engine, if_exists='append', index=False)
    fact_column.to_sql(name="fact_event", con=engine, if_exists='append', index=False)

if __name__ == "__main__":
    weather_load()
    print("Data loaded successfully!")

#RECOMMIT AFTER TIMESTAMP FIX!!!!!!!!!!!!!!!