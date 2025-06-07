
import os
import sys
import requests
import re
import subprocess
from datetime import datetime
from bs4 import BeautifulSoup


REPO_URL = "https://raw.githubusercontent.com/keerooxx/weather/main/weather.py"
UPDATE_INTERVAL = 86400  

def check_update():
    """Перевіряє наявність оновлень на GitHub"""
    try:

        local_mtime = os.path.getmtime(__file__) if os.path.exists(__file__) else 0
        
        if (datetime.now().timestamp() - local_mtime) > UPDATE_INTERVAL:
            print("\033[1;33mПеревірка оновлень...\033[0m")
            response = requests.head(REPO_URL)
            remote_size = int(response.headers.get('Content-Length', 0))

         
            local_size = os.path.getsize(__file__) if os.path.exists(__file__) else 0
            if remote_size != local_size:
                print("\033[1;32mЗнайдено оновлення! Завантаження...\033[0m")
                new_script = requests.get(REPO_URL).text
                
                with open(__file__, 'w') as f:
                    f.write(new_script)
                
                print("\033[1;32mОновлено успішно! Перезапуск...\033[0m")
                os.execl(sys.executable, sys.executable, *sys.argv)
    
    except Exception as e:
        print(f"\033[1;31mПомилка оновлення: {str(e)}\033[0m")

def get_weather(city):
    """Отримує погоду з sinoptik.ua"""
    try:
      
        search_url = f"https://sinoptik.ua/поиск?q={city}"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
       
        first_result = soup.find('div', class_='searchBlock')
        if not first_result:
            return "Місто не знайдено"
            
        city_link = first_result.find('a')['href']
        city_id = city_link.split('/')[-1]
        
       
        weather_url = f"https://sinoptik.ua{city_link}"
        response = requests.get(weather_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
       
        today = soup.find('div', class_='main loaded')
        temperature = today.find('p', class_='today-temp').text.strip()
        description = today.find('div', class_='description').text.strip()
        
       
        details = today.find('div', class_='weatherDetails')
        params = [p.text.strip() for p in details.find_all('tr')]
        
       
        result = f"\033[1;34mПогода в {city.capitalize()}:\033[0m\n"
        result += f"\033[1;36m{temperature}\033[0m\n"
        result += f"{description}\n\n"
        result += "\033[1;34mДеталі:\033[0m\n"
        result += "\n".join(params)
        
        return result
        
    except Exception as e:
        return f"\033[1;31mПомилка: {str(e)}\033[0m"

def main():
    """Головна функція"""
  
    check_update()
    
    
    COLORS = {
        'header': '\033[1;34m',
        'success': '\033[1;32m',
        'reset': '\033[0m'
    }
    
 
    os.system('clear')
    
  
    print(f"{COLORS['header']}=== Швидкий погодний скрипт ==={COLORS['reset']}")
    print(f"{COLORS['header']}(Дані з sinoptik.ua){COLORS['reset']}\n")
    

    city = input("Введіть назву міста: ").strip() or "Київ"
    
   
    print(f"\n{COLORS['success']}Запит даних...{COLORS['reset']}")
    weather_data = get_weather(city)
    

    print("\n" + weather_data)

def install_dependencies():
    """Встановлює необхідні залежності"""
    print("\033[1;34mВстановлення залежностей...\033[0m")
    commands = [
        "pkg update -y",
        "pkg install python -y",
        "pip install requests beautifulsoup4"
    ]
    
    for cmd in commands:
        print(f"\033[1;33mВиконання: {cmd}\033[0m")
        subprocess.run(cmd, shell=True, check=True)
    
    print("\033[1;32mЗалежності встановлено успішно!\033[0m")

if __name__ == "__main__":

    try:
        import requests
        import bs4
        main()
    except ImportError:
        install_dependencies()
        main()
