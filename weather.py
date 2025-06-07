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


day_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def get_weather(city):
    print(colored(f"\nПрогноз погоди для: {city.capitalize()}\n", 'cyan'))

    
    geo_url = f"https://nominatim.openstreetmap.org/search?city={city}&country=Україна&format=json"
    headers = {'User-Agent': 'weather-termux-script'}
    try:
        response = requests.get(geo_url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(colored(f"Помилка під час отримання координат: {e}", 'red'))
        return False

    data = response.json()
    if not data:
        print(colored("Місто не знайдено або введено некоректно.", 'red'))
        return False

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
        return False

    wdata = wres.json()
    days = wdata['daily']['time']
    max_temps = wdata['daily']['temperature_2m_max']
    min_temps = wdata['daily']['temperature_2m_min']
    rain = wdata['daily']['precipitation_sum']

   
    day_data = []
    for i in range(len(days)):
        date_obj = datetime.strptime(days[i], "%Y-%m-%d")
        eng_day = date_obj.strftime('%A')
        ukr_day = ukrainian_days.get(eng_day, eng_day)
        day_data.append({
            'eng_day': eng_day,
            'ukr_day': ukr_day,
            'min_temp': min_temps[i],
            'max_temp': max_temps[i],
            'rain': rain[i]
        })

  
    day_data_sorted = sorted(day_data, key=lambda x: day_order.index(x['eng_day']))

    table = []
    for d in day_data_sorted:
        row = [
            colored(d['ukr_day'], 'yellow'),
            colored(f"{d['min_temp']:.1f}°C", 'blue'),
            colored(f"{d['max_temp']:.1f}°C", 'red'),
            colored(f"{d['rain']:.1f} мм", 'green')
        ]
        table.append(row)

    headers = [
        colored("День", 'white', attrs=['bold']),
        colored("Мін. темп", 'white'),
        colored("Макс. темп", 'white'),
        colored("Опади", 'white')
    ]

    print(tabulate(table, headers=headers, tablefmt="grid"))
    return True


def main():
    print(colored("\n=== Прогноз погоди ===", 'magenta', attrs=['bold']))
    while True:
        city = input("\nВведіть назву міста українською: ").strip()
        if not city:
            print(colored("Назва міста не може бути порожньою.", 'red'))
            continue
        success = get_weather(city)
        if success:
            again = input("\nБажаєте подивитись погоду для іншого міста? (так/ні): ").strip().lower()
            if again not in ['так', 'yes', 'y']:
                print(colored("Дякую, до побачення!", 'cyan'))
                break
        else:
            print(colored("Спробуйте ввести місто ще раз.", 'yellow'))

if __name__ == '__main__':
    main()
