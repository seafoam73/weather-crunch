import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from transform import transform_weather

# Load environment variables from .env
load_dotenv()

#retreives DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

#uses SQLalchemy to translate between pandas and PostgreSQL. Sets up the instructions to connect to to_sql()
engine = create_engine(DATABASE_URL)

#calls the transform.py transformed data and puts them in the respective SQL tables
def weather_load():
    df = transform_weather()
    df.to_sql(name="dim_city", con=engine, if_exists='append', index=False)
    df.to_sql(name="dim_weather", con=engine, if_exists='append', index=False)
    df.to_sql(name="dim_date", con=engine, if_exists='append', index=False)
    df.to_sql(name="fact_event", con=engine, if_exists='append', index=False)

if __name__ == "__main__":
    weather_load()
    print("Data loaded successfully!")