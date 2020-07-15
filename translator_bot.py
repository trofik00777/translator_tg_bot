import requests
import telebot
from telebot import types
from telebot.types import Message, CallbackQuery

TOKEN = "1377088297:AAGwRQ_Eifcue7YRS_lw7zmb3Vb3URb3H_I"

url = "https://translate.yandex.net/api/v1.5/tr.json/translate"
key = "trnsl.1.1.20170208T075729Z.cdce3a3db4e5107e.64d6e22f16d94000532fc4f6ab51fe55704ea7b6"

bot = telebot.TeleBot(TOKEN)

lang = dict()

m = types.InlineKeyboardMarkup()
butt = types.InlineKeyboardButton(text="Русский", callback_data="ru")
butt1 = types.InlineKeyboardButton(text="English", callback_data="en")
m.add(butt)
m.add(butt1)


@bot.message_handler(commands=["start", "help"])
def start(message: Message):
    lang[f"{message.from_user.id}"] = "ru"
    bot.send_message(message.chat.id, "Привет, это тестовый бот-переводчик, на какой язык переводить все?", reply_markup=m)


@bot.callback_query_handler(func=lambda call: True)
def callback(call: CallbackQuery):
    print(call)
    bot.answer_callback_query(callback_query_id=call.id, text="Done!", show_alert=False)
    if call.message:
        lang[f"{call.from_user.id}"] = call.data


@bot.message_handler(content_types=["text"])
def translate(message: Message):
    text = message.text
    tr_text = requests.post(url=url, data={"key": key, "lang": lang[f'{message.from_user.id}'], "text": text}).json()["text"]
    bot.reply_to(message=message, text=tr_text)


bot.polling()
