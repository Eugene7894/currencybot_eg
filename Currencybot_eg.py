import telebot

from extensions import APIException, CurrencyConverter
from config import keys, TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def helper(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду в формате:\n<имя валюты, цену которой нужно узнать> \
    <имя валюты, в которой нужно узнать цену первой валюты> <количество первой валюты>\n\
    Пример: евро рубль 30 .\n\
    Увидеть список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands='values')
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys:
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types='text')
def convert(message: telebot.types.Message):

    try:
        curr_values = message.text.split()
        if len(curr_values) != 3:
            raise APIException('Неверное кол-во параметров')

        total_base = CurrencyConverter.get_price(*curr_values)
    except APIException as e:
        bot.reply_to(message, f'Ошибка ввода:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')
    else:
        bot.send_message(message.chat.id, total_base)


bot.polling(none_stop=True)




