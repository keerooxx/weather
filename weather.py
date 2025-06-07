import requests
from bs4 import BeautifulSoup

def get_weather(city):
    url = f'https://sinoptik.ua/погода-{city.lower()}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Не вдалося отримати дані для міста {city}. Перевірте правильність введення.")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    weather = soup.find('div', class_='today-temp')
    if weather:
        temperature = weather.find('p', class_='today-temp__value').text.strip()
        description = weather.find('div', class_='today-temp__descr').text.strip()
        print(f"Погода в місті {city.capitalize()}:\nТемпература: {temperature}\nОпис: {description}")
    else:
        print(f"Не вдалося знайти інформацію про погоду для міста {city}. Перевірте правильність введення.")

if __name__ == '__main__':
    print("🌤️ Погодний скрипт для Termux")
    city = input("Введіть назву міста: ")
    get_weather(city)
