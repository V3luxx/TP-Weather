import requests
import json
from config import API_KEY
from datetime import datetime


def get_weather_data(city, country_code):
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city},{country_code}&units=metric&appid={API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Erreur lors de l'appel à l'API:", response.status_code)
        return None

def generate_forecast_json(data):
    if data:
        location_code = data['city']['country']
        location_city = data['city']['name']
        forecast_location = f"{location_city}({location_code})"
        
        forecast_details: dict[int, list[float]] = {}
        
        for forecast in data['list']:
            date_time = forecast['dt_txt']
            date_formated = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").day
            if not date_formated in forecast_details.keys():
                forecast_details[date_formated] = []
            temperature = float(forecast['main']['temp'])
            forecast_details[date_formated].append(temperature)
            forecast_min_temp = forecast['main']['temp_min']
            forecast_max_temp = forecast['main']['temp_max']

        formatted_forecast_details = []
        for key, values in forecast.items():
            formatted_forecast_details.append({
                "date": date_formated,
                "temp": temperature,  # Remettre la valeur à l'échelle d'origine
                "measure_count": values['count']
            })

        # Construction de l'objet JSON final
        forecast_json = {
            "forecast_location": forecast_location,
            "forecast_min_temp": forecast_min_temp,
            "forecast_max_temp": forecast_max_temp,
            "forecast_details": formatted_forecast_details
        }
        
        return forecast_json

def main():
    city = "Marseille"  # input("Entrez le nom de la ville dont vous voulez connaître la météo : ")
    country_code = "FR" # input("Entrez le code du pays (exemple: FR) : ")
    weather_data = get_weather_data(city, country_code)
    forecast_json = generate_forecast_json(weather_data)

    if forecast_json:
        print(json.dumps(forecast_json, indent=4, ensure_ascii=False))  # Affiche le JSON formaté

if __name__ == "__main__":
    main()
