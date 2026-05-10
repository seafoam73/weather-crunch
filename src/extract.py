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
URL_A = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=imperial"
URL_B = f"http://api.openweathermap.org/geo/1.0/direct?q=Springfield,MO,US&limit=1&appid={API_KEY}"

def extract_weather():
    response_A = requests.get(URL_A)
    response_B = requests.get(URL_B)
    data_A = response_A.json()
    data_B = response_B.json()
    print(json.dumps(data_A, indent=4))
    print(json.dumps(data_B, indent=4))
    return data_A, data_B


#only run extract_weather() if this file is being run directly. The function only fires when you explicitly run python src/extract.py.
if __name__ == "__main__":
    extract_weather()