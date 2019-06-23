import telebot
import requests
import re
import variables as var
import bs4



    
bot = telebot.TeleBot(var.bot_token)

def get_kurs_onDate_usd(Date):
    try:
        response = requests.get(var.bank_url_usd.format(Date))
        if response.status_code == 200:
            return ('Подключение установлено')
        elif response.status_code == 404:
            return ('Страница не найдена')
        elif response.status_code == 500:
            return ('Внутренняя ошибка сервера')
        else:
            return ('Иная ошибка')
    except ConnectionError:
        return ('Ошибка подключения')
    except requests.exceptions.InvalidSchema:
        return ('Ошибка В URL')
    finally:
        return response.json()

def get_kurs_onDate_euro(Date):
    try:
        response = requests.get(var.bank_url_euro.format(Date))
        if response.status_code == 200:
            return ('Подключение установлено')
        elif response.status_code == 404:
            return ('Страница не найдена')
        elif response.status_code == 500:
            return ('Внутренняя ошибка сервера')
        else:
            return ('Иная ошибка')
    except ConnectionError:
        return ('Ошибка подключения')
    except requests.exceptions.InvalidSchema:
        return ('Ошибка В URL')
    finally:
        return response.json()

def get_kurs_usd(json_answer): 
    Cur_Rate = json_answer['Cur_OfficialRate']
    return Cur_Rate 

def get_kurs_euro(json_answer):
    Cur_Rate = json_answer['Cur_OfficialRate']  
    return Cur_Rate

def weather():
    try:
        response = requests.get(var.weather_url)
        if response.status_code == 200:
            return ('Подключение установлено')
        elif response.status_code == 404:
            return ('Страница не найдена')
        elif response.status_code == 500:
            return ('Внутренняя ошибка сервера')
        else:
            return ('Иная ошибка')
    except ConnectionError:
        return ('Ошибка подключения')
    except requests.exceptions.InvalidSchema:
        return ('Ошибка В URL')
    finally:
        return response.json()

def temperature_min(json_answer):
    minimum = json_answer['main']['temp_min']
    return minimum

def temperature_max(json_answer):
    maximum = json_answer['main']['temp_max']
    return maximum

def get_from_habr():
    response = requests.get(var.habr_url)
    return response.text

def get_pars():
    text = bs4.BeautifulSoup(get_from_habr(), 'html.parser')
    return text

def Title():
    title = get_pars().select('a.post__title_link')
    length = len(title)
    i = 0
    New_title = []
    while i < length:
        text = str(title[i])
        New_title.append(re.sub('<[^>]*>', '', text))
        i += 1
    return New_title



@bot.message_handler(content_types=["text"])
def send_message(message):
    if message.text.lower() == 'курс':   
        bot.send_message(message.chat.id, 'Введите дату в формате год-месяц-число')
        print(message.text)
    elif message.text.lower() == 'погода':
        minimum = temperature_min(weather())
        maximum = temperature_max(weather())
        bot.send_message(message.chat.id, f'Температура на сегодня: минимальная - {minimum}, максимальная - {maximum}')
    elif message.text.lower() == 'хабр':
        i = 0
        length = len(Title())
        title = Title()
        while i < length:
            bot.send_message(message.chat.id, title[i])
            i += 1
    else:
        Date = message.text
        USD = get_kurs_usd(get_kurs_onDate_usd(Date))
        EURO = get_kurs_euro(get_kurs_onDate_euro(Date))
        bot.send_message(message.chat.id, f'На запрошенную дату курс составляет {EURO} за один евро, {USD} за один доллар')

bot.polling()

