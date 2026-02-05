import requests


running = True
key = "HZ5AV8EGJJC4S62TQL45YD2WM"
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





