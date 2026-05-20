import pandas as pd
from datetime import datetime

#takes the 7 fields we want from the weather API and the country/state deatils from the geo API and pulls them from the API JSONs and into a DataFrame
def transform_weather(data_A, data_B):
    weather_events = {
        "city_name": data_A["name"],
        "temperature": data_A["main"]["temp"],
        "pressure": data_A["main"]["pressure"],
        "humidity": data_A["main"]["humidity"],
        "weather_name": data_A["weather"][0]["description"],
        "wind_speed": data_A["wind"]["speed"],
        "full_datetime": datetime.fromtimestamp(data_A["dt"]),
        "country": data_B[0]["country"],
        "state": data_B[0]["state"]
    }
    weather_table = pd.DataFrame([weather_events])
    weather_table['year'] = weather_table['full_datetime'].dt.year
    weather_table['month'] = weather_table['full_datetime'].dt.month
    weather_table['day'] = weather_table['full_datetime'].dt.day
    weather_table['hour'] = weather_table['full_datetime'].dt.hour
    return weather_table

def iterate_weather(x, y):
    frames = []
    for a, b in zip(x, y):
        frames.append(transform_weather(a, b))
    full_table = pd.concat(frames)
    return full_table
        

#calls the function with the variables below only when the file itself is ran. As opposed to being imported as intended
if __name__ == "__main__":
    sample_A = [{
        "name": "Dallas",
        "main": {"temp": 76, "pressure": 1012, "humidity": 42},
        "weather": [{"description": "mostly cloudy"}],
        "wind": {"speed": 2.99},
        "dt": 1777578140
        },
        {
        "name": "Louisville",
        "main": {"temp": 68, "pressure": 999, "humidity": 60},
        "weather": [{"description": "partly cloudy"}],
        "wind": {"speed": 1.05},
        "dt": 1887578140
        }
        ]
    sample_B = [[{
        "country": "US",
        "state": "Texas"
    }],
    [{
       "country": "US",
        "state": "Kentucky" 
    }]]
    print(iterate_weather(sample_A, sample_B))