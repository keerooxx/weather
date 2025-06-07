import requests
from termcolor import colored
from tabulate import tabulate
from datetime import datetime
import locale


try:
    locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8')
except:
    locale.setlocale(locale.LC_TIME, '')

def get_weather(city):
    print(colored(f"\nПрогноз погоди для: {city.capitalize()}\n", 'cyan'))


    geocode_url = f"https://geocode.maps.co/search?q={city},Ukraine&format=json"
    response = requests.get(geocode_url)
    if response.status_code != 200 or not response.json():
        print(colored("❗ Місто не знайдено. Перевірте написання.", 'red'))
        return

    data = response.json()[0]
    lat, lon = data['lat'], data['lon']

  
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&daily=temperature_2m_max,"
        f"temperature_2m_min,precipitation_sum&temperature_unit=celsius"
        f"&precipitation_unit=mm&timezone=Europe/Kiev"
    )
    wres = requests.get(weather_url)
    if wres.status_code != 200:
        print(colored("❗ Не вдалося отримати погоду.", 'red'))
        return

    wdata = wres.json()
    days = wdata['daily']['time']
    max_temps = wdata['daily']['temperature_2m_max']
    min_temps = wdata['daily']['temperature_2m_min']
    rain = wdata['daily']['precipitation_sum']


    table = []
    for i in range(len(days)):
        date_obj = datetime.strptime(days[i], "%Y-%m-%d")
        day_name = date_obj.strftime('%A').capitalize()
        row = [
            colored(day_name, 'yellow'),
            colored(f"{min_temps[i]:.1f}°C", 'blue'),
            colored(f"{max_temps[i]:.1f}°C", 'red'),
            colored(f"{rain[i]:.1f} мм", 'green')
        ]
        table.append(row)

    headers = [
        colored("День", 'white', attrs=['bold']),
        colored("Мін. темп", 'white'),
        colored("Макс. темп", 'white'),
        colored("Опади", 'white')
    ]

    print(tabulate(table, headers=headers, tablefmt="grid"))

if __name__ == '__main__':
    print(colored("\n=== Прогноз погоди ===", 'magenta', attrs=['bold']))
    city = input("Введіть назву міста українською: ")
    get_weather(city)
