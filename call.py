import requests
import json
from config import API_KEY
from datetime import datetime
import click
from loguru import logger

logger.add("weather_forecast.log", rotation="1 MB", retention="5 days", level="INFO")


class WeatherForecast:
    def __init__(self, city, country_code):
        self.city = city
        self.country_code = country_code
        self.weather_data = None
        self.forecast_json = None

    def get_weather_data(self):
        url = f'https://api.openweathermap.org/data/2.5/forecast?q={self.city},{self.country_code}&units=metric&appid={API_KEY}'
        response = requests.get(url)

        if response.status_code == 200:
            logger.info("Données météo récupérées avec succès.")
            self.weather_data = response.json()
        else:
            logger.error(f"Erreur lors de l'appel à l'API: {response.status_code}")
            print("Erreur lors de l'appel à l'API:", response.status_code)

    def generate_forecast_json(self):
        if self.weather_data:
            location_code = self.weather_data['city']['country']
            location_city = self.weather_data['city']['name']
            forecast_location = f"{location_city}({location_code})"

            forecast_summary = {}
            min_temps = []
            max_temps = []

            for forecast in self.weather_data['list']:
                date_time = forecast['dt_txt']
                forecast_min_temp = forecast['main']['temp_min']
                forecast_max_temp = forecast['main']['temp_max']
                temperature = float(forecast['main']['temp'])

                # Convertir date_time en objet datetime
                date_obj = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
                date_str = date_obj.strftime("%Y-%m-%d")  # Format de la date

                # Ajouter les températures minimales et maximales
                min_temps.append(forecast_min_temp)
                max_temps.append(forecast_max_temp)

                # Regrouper les températures par date
                if date_str not in forecast_summary:
                    forecast_summary[date_str] = {'temperatures': [], 'measure_count': 0}

                forecast_summary[date_str]['temperatures'].append(temperature)
                forecast_summary[date_str]['measure_count'] += 1

            # Créer les détails de prévision formatés
            format_forecast_details = []
            for date, data in forecast_summary.items():
                avg_temp = sum(data['temperatures']) / data['measure_count']
                format_forecast_details.append({
                    "date": date,
                    "temp": round(avg_temp, 1),
                    "measure_count": data['measure_count']
                })

            self.forecast_json = {
                "forecast_location": forecast_location,
                "forecast_min_temp": min(min_temps),
                "forecast_max_temp": max(max_temps),
                "forecast_details": format_forecast_details
            }

            filename = "results.json"
            with open(filename, 'w') as json_file:
                json.dump(self.forecast_json, json_file, indent=4)
                logger.info(f"Les prévisions ont été écrites dans le fichier '{filename}'.")


@click.command()
def main():
    BLUE = "\033[34m"
    YELLOW = "\033[32m"
    MAGENTA = "\033[35m"

    print(BLUE + "(((((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))))))))")
    city = click.prompt("Entrez le nom de la ville dont vous voulez connaître la météo : ")
    print(MAGENTA + "(((((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))))))))")
    country_code = click.prompt("Entrez le code du pays (exemple: FR) : ")
    print(YELLOW + "(((((((((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))))))))")

    forecast = WeatherForecast(city, country_code)
    forecast.get_weather_data()
    forecast.generate_forecast_json()

    if forecast.forecast_json:
        logger.info("Prévisions météo générées avec succès.")


if __name__ == "__main__":
    main()
