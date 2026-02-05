import requests
from dotenv import load_dotenv
import os 
import redis


running = True

load_dotenv()
r = redis.Redis(host='cache', port=6379, decode_responses=True)
key = os.environ.get("WEATHER_APP_KEY")
location = os.environ.get("CITY_NAME", "Warsaw")



def get_weather():
    
    cached_data = r.get(location)

    if cached_data:
        print(f"--- Dane pobrane z CACHE (Redis) dla: {location} ---")
        print(cached_data)
        return
    
    print(f"--- Brak danych w Cache. Pytam API dla: {location} ---")

    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?key={key}'

    try:
        x = requests.get(url)

        if x.status_code == 200:
            data = x.json()

            temp = data['currentConditions']['temp']
            description = data['description']
            address = data['resolvedAddress']

            r.set(f"{location}", temp)

            print(f"Miasto: {address}")
            print(f"Temperatura: {temp}°C")
            print(f"Opis: {description}")
    except Exception as e:
        print(f"Wystąpił błąd połączenia: {e}") 


    
if __name__ == "__main__":
    get_weather()





