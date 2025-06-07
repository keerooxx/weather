import requests
from bs4 import BeautifulSoup

def get_weather(city):
    url = f'https://sinoptik.ua/погода-{city.lower()}'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Не вдалося отримати дані для міста '{city}'.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    temp_tag = soup.select_one('.today-temp .today-temp__value')
    descr_tag = soup.select_one('.today-temp .today-temp__descr')

    if temp_tag and descr_tag:
        temperature = temp_tag.text.strip()
        description = descr_tag.text.strip()
        print(f"\n🌤️ Погода в місті {city.capitalize()}:")
        print(f"🌡️ Температура: {temperature}")
        print(f"📋 Опис: {description}\n")
    else:
        print(f"⚠️ Інформацію не знайдено. Можливо, місто '{city}' недоступне.")

if __name__ == '__main__':
    print("=== 🌦️ Погодний скрипт для Termux ===")
    city = input("🔎 Введіть назву міста українською: ")
    get_weather(city)
