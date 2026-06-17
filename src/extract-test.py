#pulls the current weather for 4 of the most populated cities in MO & its state capital, and pulls weather information about those cities at that moment
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

missouri_prime = [
    {"City": "Columbia", "State": "MO", "Country": "US"}, 
    {"City": "Kansas City", "State": "MO", "Country": "US"}, 
    {"City": "Jefferson City", "State": "MO", "Country": "US"}, 
    {"City": "Springfield", "State": "MO", "Country": "US"}, 
    {"City": "St. Louis", "State": "MO", "Country": "US"}
]


def url_feed(x):
    city_url= [] 
    for i in x:
        city_url.append(f"http://api.openweathermap.org/geo/1.0/direct?q={i['City']},{i['State']},{i['Country']}&limit=1&appid={API_KEY}")
    return city_url


def lat_lon(data):
    url_plug = []
    for i in data:
        response = requests.get(i)
        my_list = response.json()
        LAT = my_list[0]["lat"]
        LON = my_list[0]["lon"]
        url_plug.append(f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=imperial")
    return url_plug

#takes the geo URLs and the city weather URls, combines them and puts all the data into a list
def extract_weather(x, y):
    data_a =[]
    data_b =[]
    for a, b in zip(x, y):
        response_a = requests.get(a)
        response_b = requests.get(b)
        combined_data_a = response_a.json()
        combined_data_b = response_b.json()
        data_a.append(combined_data_a)
        data_b.append(combined_data_b)
    return data_a, data_b

#only run extract_weather() if this file is being run directly. The function only fires when you explicitly run python src/extract.py.
if __name__ == "__main__":
    extract_weather(url_feed(missouri_prime), lat_lon(url_feed(missouri_prime)))


