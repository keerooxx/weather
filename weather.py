
import os
import sys
import requests
from urllib.parse import quote

def main():
 
    COLORS = {
        'header': '\033[1;34m',
        'success': '\033[1;32m',
        'error': '\033[1;31m',
        'warning': '\033[1;33m',
        'reset': '\033[0m'
    }
    
    
    os.system('clear')
    

    print(f"{COLORS['header']}=== Погодний скрипт для Termux ==={COLORS['reset']}")
    print(f"{COLORS['header']}(Дані з wttr.in){COLORS['reset']}\n")
    
 
    try:
        requests.get('http://google.com', timeout=5)
    except requests.ConnectionError:
        print(f"{COLORS['error']}Помилка: Немає інтернет-з'єднання!{COLORS['reset']}")
        sys.exit(1)
    
 
    city = input("Введіть назву міста (наприклад Київ): ").strip()
    
    if not city:
        city = "Київ"
        print(f"\n{COLORS['warning']}Використовується місто за замовчуванням: Київ{COLORS['reset']}")
    
  
    encoded_city = quote(city)
    
    print(f"\n{COLORS['success']}Завантаження даних для {city}...{COLORS['reset']}\n")
    
    try:
        
        url = f"http://wttr.in/{encoded_city}?lang=uk"
        response = requests.get(url, headers={'User-Agent': 'curl/7.64.1'})
        
       
        if response.status_code == 200:
            print(response.text)
        else:
            print(f"{COLORS['error']}Помилка: Не вдалося отримати дані (код {response.status_code}){COLORS['reset']}")
            print("Можливі причини:")
            print("- Неправильна назва міста")
            print("- Тимчасова недоступність сервісу")
    
    except Exception as e:
        print(f"\n{COLORS['error']}Критична помилка: {str(e)}{COLORS['reset']}")

if __name__ == "__main__":
    main()