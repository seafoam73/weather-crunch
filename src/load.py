import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

#where is df coming from?
def weather_load():
    df = transform_weather()
    df.to_sql(name="dim_city", con=engine, if_exists='append', index=False)
    df.to_sql(name="dim_weather", con=engine, if_exists='append', index=False)
    df.to_sql(name="dim_date", con=engine, if_exists='append', index=False)
    df.to_sql(name="fact_event", con=engine, if_exists='append', index=False)

if __name__ == "__main__":
    sample = 
    
    print()