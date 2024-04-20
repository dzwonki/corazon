#pylint:disable=E0001
import telebot
import requests
import json
from telebot import types
from flask import Flask, request
from threading import Thread

app = Flask('')

def get_balance(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'language': 'AR',
        'request-id': '2dfefb8b-b2fa-445a-a49c-113d2d880b2f',
        'flavour-type': 'gms',
        'Host': 'ibiza.ooredoo.dz',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/4.9.3'
    }
    response = requests.get('https://ibiza.ooredoo.dz/api/v1/mobile-bff/users/balance', headers=headers).text
    response_dict = json.loads(response)
    return response_dict

bot = telebot.TeleBot("7058539969:AAHL7AG9TBJ9qhi1Bl3dx8FSBb8QflPcpZs")

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(chat_id=message.chat.id, text='مرحبا ارسل توكنك لمعرفة رصيدك')

@bot.message_handler(func=lambda message: 'e' in message.text)
def handle_balance(message):
    lines = message.text
    token = lines
    balance_data = get_balance(token)
    if 'accounts' in balance_data:
        for account in balance_data['accounts']:
            bot.send_message(chat_id=message.chat.id, text=f"{account['label']}: {account['value']}")
    else:
        bot.send_message(message.chat.id, 'حدث خطأ في الطلب. يرجى التحقق من التوكن والمحاولة مرة أخرى.')

@app.route('/')
def home():
    return "<b>telegram @X0_XV</b>"

def run():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
