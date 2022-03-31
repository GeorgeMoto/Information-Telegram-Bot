import telebot
from DATA import *
from telebot import types

bot = telebot.TeleBot("5263039063:AAEKR__jHHkhnlc5CmhcYR-q4LNJQXyUpEE")


@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    key_information = types.InlineKeyboardButton(text="🧐 Что это такое?", callback_data="key_information")
    key_download = types.InlineKeyboardButton(text="🚀 Где скачать софт", callback_data="key_download")
    key_important_info = types.InlineKeyboardButton(text="‼️Важная информация", callback_data="key_important_info")
    key_payments = types.InlineKeyboardButton(text="💸️Оплата", callback_data="key_payments")

    keyboard.add(key_information, key_download, key_important_info, key_payments)
    bot.send_message(message.chat.id, text=greetings, parse_mode="html",
                     reply_markup=keyboard)


@bot.message_handler(commands=["help"])
def start(message):
    bot.send_message(message.chat.id, text=help_text, parse_mode="html")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):

    if call.data == "key_information":
        bot.send_message(call.message.chat.id, information_text, parse_mode="html")
    elif call.data == "key_download":
        bot.send_message(call.message.chat.id, download_text, parse_mode="html")
    elif call.data == "key_important_info":
        bot.send_message(call.message.chat.id, important_info_text, parse_mode="html")
    elif call.data == "key_payments":
        bot.send_message(call.message.chat.id, payments_text, parse_mode="html")



bot.polling(none_stop=True)