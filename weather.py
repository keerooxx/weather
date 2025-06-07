import requests
from termcolor import colored
from tabulate import tabulate
from datetime import datetime


ukrainian_days = {
    'Monday': 'Понеділок',
    'Tuesday': 'Вівторок',
    'Wednesday': 'Середа',
    'Thursday': 'Четвер',
    'Friday': "Пʼятниця",
    'Saturday': 'Субота',
    'Sunday': 'Неділя'
}

def get_weather(city):
    print(colored(f"\nПрогноз погоди для: {city.capitalize()}\n", 'cyan'))

    
    geo_url = f"https://nominatim.openstreetmap.org/search?city={city}&country=Україна&format=json"
    headers = {'User-Agent': 'weather-termux-script'}
    try:
        response = requests.get(geo_url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(colored(f"Помилка під час отримання координат: {e}", 'red'))
        return

    data = response.json()
    if not data:
        print(colored("Місто не знайдено або введено некоректно.", 'red'))
        return

    lat, lon = data[0]['lat'], data[0]['lon']

   
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
        f"&temperature_unit=celsius&precipitation_unit=mm&timezone=Europe/Kiev"
    )
    try:
        wres = requests.get(weather_url, timeout=10)
        wres.raise_for_status()
    except Exception as e:
        print(colored(f"Помилка під час отримання погоди: {e}", 'red'))
        return

    wdata = wres.json()
    days = wdata['daily']['time']
    max_temps = wdata['daily']['temperature_2m_max']
    min_temps = wdata['daily']['temperature_2m_min']
    rain = wdata['daily']['precipitation_sum']

   
    table = []
    for i in range(len(days)):
        date_obj = datetime.strptime(days[i], "%Y-%m-%d")
        eng_day = date_obj.strftime('%A')
        ukr_day = ukrainian_days.get(eng_day, eng_day)
        row = [
            colored(ukr_day, 'yellow'),
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
    city = input("Введіть назву міста українською: ").strip()
    if city:
        get_weather(city)
    else:
        print(colored("Назва міста не може бути порожньою.", 'red'))
