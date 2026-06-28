#pulls 5 large Missouri cities including the state capital, and pulls the current weather information from those cities
import requests
import json
import os
#Only necessary when the .env variables are not run externally i.e. Github. Used when ran locally
#from dotenv import load_dotenv
#Load environment variables from .env
#load_dotenv() # handled by load.py / GitHub Actions sets env vars directly

#Creates a list of city dictionaries used as the main keys to pull the data from OpenWeatherMap
missouri_prime = [
    {"City": "Columbia", "State": "MO", "Country": "US"}, 
    {"City": "Kansas City", "State": "MO", "Country": "US"}, 
    {"City": "Jefferson City", "State": "MO", "Country": "US"}, 
    {"City": "Springfield", "State": "MO", "Country": "US"}, 
    {"City": "St. Louis", "State": "MO", "Country": "US"}
]

#creates the geo URL's to provide the lat/lon for the weather api, and the country/state for the transform.py function
def url_feed(cities):
    API_KEY = os.getenv("API_KEY")
    city_url= [] 
    for i in cities:
        city_url.append(f"http://api.openweathermap.org/geo/1.0/direct?q={i['City']},{i['State']},{i['Country']}&limit=1&appid={API_KEY}")
    return city_url

#Utilizes each city's lat/lon to build the weather URLs that are extracted
def lat_lon(data):
    API_KEY = os.getenv("API_KEY")
    url_plug = []
    for i in data:
        response = requests.get(i)
        my_list = response.json()
        if not my_list:
            continue
        LAT = my_list[0]["lat"]
        LON = my_list[0]["lon"]
        url_plug.append(f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=imperial")
    return url_plug


#takes the geo URLs and the city weather URls, returns both, geo as a list of list and weather as a list of dictionaries
def extract_weather(geo_url, weather_url):
    data_geo =[]
    data_weather =[]
    for a, b in zip(geo_url, weather_url):
        response_a = requests.get(a)
        response_b = requests.get(b)
        combined_data_a = response_a.json()
        combined_data_b = response_b.json()
        data_geo.append(combined_data_a)
        data_weather.append(combined_data_b)
    return data_geo, data_weather
    

#only run extract_weather() if this file is being run directly. The function only fires when you explicitly run python src/extract.py.
if __name__ == "__main__":
    urls = url_feed(missouri_prime)
    extract_weather(urls, lat_lon(urls))
    