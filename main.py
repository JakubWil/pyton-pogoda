import requests
from dotenv import load_dotenv
import os 
import redis
import json
import re



r = redis.Redis(host='cache', port=6379, decode_responses=True)


load_dotenv()

key = os.environ.get("WEATHER_APP_KEY")
location = os.environ.get("CITY_NAME", "Warsaw")

def api_call(city, key):
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?key={key}'

    try:
        x = requests.get(url)

        if x.status_code == 200:
            data = x.json()

            cityValues = {
                "temp": str(data['currentConditions']['temp']),
                "description": data['description'],
                "address": data['resolvedAddress']
            }

            print(f"Dane dla {city} pobrane z API.")
            print(f"Temperatura: {cityValues['temp']}")
            print(f"Opis: {cityValues['description']}")
            print(f"Adres: {cityValues['address']}")

            

            r.set(f"{city}", json.dumps(cityValues))
            print(f"Dane dla {city} zapisane w Cache (Redis).")

           
    except Exception as e:
        print(f"Wystąpił błąd połączenia: {e}")


def get_weather():

    cities = location.split(",")

    for city in cities:

        if not re.match(r'^[a-zA-Z\s\-]+$', city):
            print(f"--- Nieprawidłowa nazwa miasta: {city} ---")
            continue

        if r.exists(city):
            print(f"--- Dane pobrane z CACHE (Redis) dla: {city} ---")
            info = json.loads(r.get(city))
            print(f"Temperatura: {info['temp']}")
            print(f"Opis: {info['description']}")
            print(f"Adres: {info['address']}")
            
        else:  
            print(f"--- Brak danych w Cache. Pytam API dla: {city} ---")
            api_call(city, key)


    
if __name__ == "__main__":
    get_weather()





