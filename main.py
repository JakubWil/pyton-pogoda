import requests
from dotenv import load_dotenv
import os 
import redis


r = redis.Redis(host='cache', port=6379, decode_responses=True)


load_dotenv()

key = os.environ.get("WEATHER_APP_KEY")
location = os.environ.get("CITY_NAME", "Warsaw")



def get_weather():

    cities = location.split(",")

    for city in cities:
    
        cached_data = r.get(city)

        print(cached_data)

        if cached_data:
            print(f"--- Dane pobrane z CACHE (Redis) dla: {city} ---")
            print(cached_data)
            
        else:
            print(f"--- Brak danych w Cache. Pytam API dla: {city} ---")

            url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?key={key}'

            try:
                x = requests.get(url)

                if x.status_code == 200:
                    data = x.json()

                    temp = data['currentConditions']['temp']
                    description = data['description']
                    address = data['resolvedAddress']

                    r.set(f"{city}", temp)

                    print(f"Miasto: {address}")
                    print(f"Temperatura: {temp}°C")
                    print(f"Opis: {description}")
                    print("---------------")
            except Exception as e:
                print(f"Wystąpił błąd połączenia: {e}") 


    
if __name__ == "__main__":
    get_weather()





