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
        min_temps = []
        max_temps = []
        
        for forecast in data['list']:
            date_time = forecast['dt_txt']
            forecast_min_temp = forecast['main']['temp_min']
            forecast_max_temp = forecast['main']['temp_max']
            temperature = float(forecast['main']['temp'])
            date_formated = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").day
            # temp min et max
            min_temps.append(forecast_min_temp)
            max_temps.append(forecast_max_temp)
            
            if date_formated not in forecast_details:
                forecast_details[date_formated] = []
            forecast_details[date_formated].append(temperature)

        format_forecast_details = []
        for day, temperatures in forecast_details.items():
            if temperatures:  # Vérifie que la liste n'est pas vide
                avg_temp = sum(temperatures) / len(temperatures)
                date_str = f"2024-10-{day:02d}"  
                format_forecast_details.append({
                    "date": date_str,
                    "avg_temp": round(avg_temp, 1),
                    "measure_count": len(temperatures)  
                })

        # Construction de l'objet JSON final
        forecast_json = {
            "forecast_location": forecast_location,
            "forecast_min_temp": min(min_temps),  # Température minimale sur la période
            "forecast_max_temp": max(max_temps),  # Température maximale sur la période
            "forecast_details": format_forecast_details
        }
        filename = "results.json"
        with open(filename, 'w') as json_file:
            json.dump(forecast_json, json_file, indent=4)  # Indentation pour une meilleure lisibilité
        
            print(f"Les prévisions ont été écrites dans le fichier '{filename}'.")
    
def main():
    city = input("Entrez le nom de la ville dont vous voulez connaître la météo : ")
    country_code = input("Entrez le code du pays (exemple: FR) : ")
    weather_data = get_weather_data(city, country_code)
    forecast_json = generate_forecast_json(weather_data)

    if forecast_json:
        print(json.dumps(forecast_json, indent=4, ensure_ascii=False))  # Affiche le JSON formaté

if __name__ == "__main__":
    main()
