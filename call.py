import requests

API_KEY = '70d31ed38befd31a6164e00bd03dd83a'

## api.openweathermap.org/data/2.5/forecast?q={city name}&appid={API key}

city = input("entrez le nom de la ville dont vous voulez connaitre la météo: ")

url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(f"Météo à {city} :")
    print(f"Température : {data}°C")
else:
    print("Erreur lors de l'appel à l'API:", response.status_code)
