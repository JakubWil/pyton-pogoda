import requests
from dotenv import load_dotenv
import os 


running = True

load_dotenv()
key = os.environ.get("WEATHER_APP_KEY")
location = "London,UK"


while running:
    location = input("Podaj nazwę miasta: ")

    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?key={key}'
    x = requests.get(url)

    if x.status_code == 200:
        data = x.json()

        temp = data['currentConditions']['temp']
        description = data['description']
        address = data['resolvedAddress']

        print(f"Miasto: {address}")
        print(f"Temperatura: {temp}°C")
        print(f"Opis: {description}")

    
    running = False





