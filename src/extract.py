#pulls the current weather for Springfield, Mo
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
# Location: Springfield, MO
LAT = 37.2090
LON = -93.2923
URL = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=imperial"

def extract_weather():
    response = requests.get(URL)
    data = response.json()
    print(json.dumps(data, indent=4))

#only run extract_weather() if this file is being run directly. The function only fires when you explicitly run python src/extract.py.
if __name__ == "__main__":
    extract_weather()