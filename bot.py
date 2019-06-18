import telebot
import requests
import variables as var



    
bot = telebot.TeleBot(var.bot_token)

def get_kurs_onDate_usd(Date):
    response = requests.get(var.bank_url_usd.format(Date))
    return response.json()

def get_kurs_onDate_euro(Date):
    response = requests.get(var.bank_url_euro.format(Date))
    return response.json()

def get_kurs_usd(json_answer): 
    Cur_Rate = json_answer['Cur_OfficialRate']
    return Cur_Rate 

def get_kurs_euro(json_answer):
    Cur_Rate = json_answer['Cur_OfficialRate']  
    return Cur_Rate

def weather():
    response = requests.get(var.weather_url)
    return response.json()

def temperature_min(json_answer):
    minimum = json_answer['main']['temp_min']
    return minimum

def temperature_max(json_answer):
    maximum = json_answer['main']['temp_max']
    return maximum

@bot.message_handler(content_types=["text"])
def send_message(message):
    if message.text.lower() == 'курс':   
        bot.send_message(message.chat.id, 'Введите дату в формате год-месяц-число')
        print(message.text)
    elif message.text.lower() == 'погода':
        minimum = temperature_min(weather())
        maximum = temperature_max(weather())
        bot.send_message(message.chat.id, f'Температура на сегодня: минимальная - {minimum}, максимальная - {maximum}')
    else:
        Date = message.text
        USD = get_kurs_usd(get_kurs_onDate_usd(Date))
        EURO = get_kurs_euro(get_kurs_onDate_euro(Date))
        bot.send_message(message.chat.id, f'На запрошенную дату курс составляет {EURO} за один евро, {USD} за один доллар')

bot.polling()

