import requests
from dotenv import load_dotenv
import os 
import redis
import json
import re

#PDF pogoda historia 
#Voluemn
#Redis dashboard

#1. Kiedy robić wirtualne środowisko, czy tylko jak pracuje lokalnie i sam w projekcie potrzebuje dane zalenznosci ? Czy robi sie takie cos ze venv wysyla na github zeby ktos inny tez mogl sie tam zalogowac i pracowac czy nie wiem wlasnie to jest to do Docker wyklucza, czy to i to mozna robic

#2. Jak mam projekt, który ma docker to ja musze na tym kompie tez miec Docker Desktop zeby moc korzystac z tego czy jakbym w venv mial docker zainstalowany to bym nie musial, bo projekt teraz mi nie dziala na innym laptopie po tym jak zrobilem git clone i robie docker compose up i dostaje Cannot connect to the Docker daemon at unix:///Users/j.wilczek/.docker/run/docker.sock. Is the docker daemon running?

#3. Co wlasnie z .env bo jesli w .gitignore daje .env to nie ma go na github, jakie sa bezpieczne metody przenoszenia .env powiedzmy ze jest tam klucz api i kazdy musi miec taki sam 

#4. Potrzebuje nauki pracy z git, bo dalej widze ze mam braki, potrzebuje zebys mi opisal taki projektowy workflow jak to wyglada. Tez potrzebuje zebys mi powiedzial co dokladnie robi git clone, kolejna rzecz odnosnie autoryzacji ja tylko raz sie autoryzuje i to robie do github tak a potem jak chce zrobic push to po prostu musze zapisac w remote dane tego repo, ale jak np nie wiem teraz bede miec jedno repo na moim kompie ale np ktos zaprosi mnie do projektu to jak bedzie autoryzacja to nie do tego repo tylko do github zeby zweryfikowal ze to ja. No i to co jeszcze tak nie ogarniam to powiedzmy ze mam kilka kont na github to jak zrobic tak ze jak pracuje nad projektem A to tam mam wysylac z konta A , projekt B z konta B ? 


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





