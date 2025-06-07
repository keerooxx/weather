import requests
from termcolor import colored

def get_weather(city):
    # Геокодування міста для отримання координат
    geocode_url = f"https://geocode.maps.co/search?q={city},Ukraine&format=json"
    response = requests.get(geocode_url)
    if response.status_code != 200 or not response.json():
        print(colored(f"Не вдалося знайти місто: {city}", 'red'))
        return

    location = response.json()[0]
    lat, lon = location['lat'], location['lon']

    # Запит до Open-Meteo API для прогнозу на 7 днів
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&temperature_unit=celsius&precipitation_unit=mm&timezone=Europe/Kiev"
    weather_response = requests.get(weather_url)
    if weather_response.status_code != 200:
        print(colored("Помилка при отриманні даних про погоду.", 'red'))
        return

    weather_data = weather_response.json()
    print(colored(f"\nПрогноз погоди на 7 днів для міста {city.capitalize()}:", 'cyan'))
    for i, day in enumerate(weather_data['daily']['time']):
        date = day
        max_temp = weather_data['daily']['temperature_2m_max'][i]
        min_temp = weather_data['daily']['temperature_2m_min'][i]
        precip = weather_data['daily']['precipitation_sum'][i]
        print(colored(f"{date}: Макс. {max_temp}°C, Мін. {min_temp}°C, Опади: {precip} мм", 'green'))

if __name__ == '__main__':
    print(colored("🌤️ Погодний скрипт для Termux", 'yellow'))
    city = input("Введіть назву міста: ")
    get_weather(city)
