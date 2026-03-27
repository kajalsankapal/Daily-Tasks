import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()
api_key = os.getenv("weather_api_key")

cities= ["Mumbai", "Pune", "Delhi", "Kolhapur", "Kolkata", "Bangalore", "Hyderabad", "Chennai", "Jaipur", "Lucknow"]
final_data = []

for city in cities:
        try:
            url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + api_key
            
            response = requests.get(url)
            if response.status_code == 404:
                print("city not found", city)
                continue

            if response.status_code == 401:
                print("invalid api key", city)
                continue
  
            if response.status_code ==200:
                 data = response.json()

            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            weather = data["weather"][0]["main"]
            time = data["dt"]
            
            celsius = round(temp - 273.15, 2) 
            time = datetime.fromtimestamp(data["dt"])

            city_data = {
                "city": city,
                "temperature": str(celsius) + "C",
                "humidity": humidity,
                "weather": weather,
                "time": str(time)
            }

            final_data.append(city_data)

        except Exception as e:
            print("error in city", city, e)

# print(final_data)
with open("weather_data.json", "w") as file:
    json.dump(final_data, file, indent=4)
    

