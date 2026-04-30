import pandas as pd
from datetime import datetime

#takes the 7 fiels we want and pulls them from the JSON and into a DataFrame
def transform_weather(data):
    weather_events = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "pressure": data["main"]["pressure"],
        "humidity": data["main"]["humidity"],
        "weather_description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"],
        "timestamp": datetime.fromtimestamp(data["dt"])
    }
    weather_table = pd.DataFrame([weather_events])
    return weather_table

#calls the function with the variable below only when the file itself is ran. As opposed to being imported as intended
if __name__ == "__main__":
    sample = {
        "name": "Dallas",
        "main": {"temp": 76, "pressure": 1012, "humidity": 42},
        "weather": [{"description": "mostly cloudy"}],
        "wind": {"speed": 2.99},
        "dt": 1777578140
        }
    
    print(transform_weather(sample))