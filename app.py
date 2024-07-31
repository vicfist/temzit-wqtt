import requests
from bs4 import BeautifulSoup
import paho.mqtt.client as mqtt
import json
import sys

# Настройки для авторизации и парсинга
login_url = "https://service.temzit.ru/login"
status_url = "https://service.temzit.ru/status"
login_data = {
    'usrLogin': "user0647",
    'usrPassw': "LJJHDPKB",
    'logmein': "sign-in"
}

# Настройки MQTT
mqtt_broker = "m9.wqtt.ru"
mqtt_port = 17378
mqtt_user = "u_CTWLDK"
mqtt_password = "FTdOoFVB"
mqtt_topic_json = "temzit/f499f2a4/json"

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/75.0.3770.142 Safari/537.36 '
    }

    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent
    # для ваших запросов используйте такую форму:
    #  User-Agent: <название-продукта> / <версия продукта> <комментарий>
user_agent = 'nameless-project / 0.0.1 (Python {0})'.format(sys.version[:5])


# открытие сессии
session = requests.Session()
# обновление headers сессии
session.headers.update({'User-Agent': user_agent})
# авторизация
response = session.post(login_url, data=login_data, timeout=3)

if response.status_code == 200:
# получаем данные
    response = session.post(status_url, timeout=3)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find('div', class_='content')
          
        # Парсинг данных
        buttons = content_div.find_all('button', class_='btn btn-lg')
        data = {}
        
        for button in buttons:
            parts = button.get_text(separator=" ").split()
            label = parts[0]
            value = parts[1]
            data[label] = value

        # Преобразование данных в JSON
        json_data = json.dumps(data)
        print(json_data)

        # Отправка данных через MQTT
        client = mqtt.Client()
        client.username_pw_set(mqtt_user, mqtt_password)
        client.connect(mqtt_broker, mqtt_port, 60)
        client.publish(mqtt_topic_json, json_data)
        client.disconnect()
    else:
        print("Не удалось получить страницу статуса.")
else:
    print("Не удалось авторизоваться.")
