import telebot
import requests
from telebot import types
from flask import Flask, request
from threading import Thread
app = Flask('')
def hh(line_3,to_line,first_line):
	m=0
	headers3= {
    'Authorization': f'Bearer {line_3}',
    'language': 'AR',
    'request-id': '9a8c8b52-98f2-49c2-b3c4-0b815dc69900',
    'flavour-type': 'gms',
    # 'Content-Length': '0',
    'Host': 'ibiza.ooredoo.dz',
    'Connection': 'Keep-Alive',
    # 'Accept-Encoding': 'gzip',
    'User-Agent': 'okhttp/4.9.3',
    'Content-Type': 'application/x-www-form-urlencoded',}
	head = {
        "Authorization": f"Bearer {to_line}",
        "language": "EN",
        "request-id": "14a32040-b8e8-4831-a255-8a7dce786dca",
        "flavour-type": "gms",
        "Content-Type": "application/json; charset=utf-8",
        "Content-Length": "50",
        "Host": "ibiza.ooredoo.dz",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.9.3"
    }
	json_data = {
        "mgmId": first_line,
        "packageId": "IBIZA_DEFAULT"
  	  }
	while True:
		m+=1
		response = requests.put('https://ibiza.ooredoo.dz/api/v1/mobile-bff/users/mgm/redeem', headers=headers3).text
		res = requests.post('https://ibiza.ooredoo.dz/api/v1/mobile-bff/users/migration', headers=head, json=json_data).text
		if m==6:
		     break
bot = telebot.TeleBot("7139841177:AAHKeNpFQLz8bOuqb9KytbocnI-zhTmpioc")
@bot.message_handler(commands=["start"])
def startt(message):
    
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    omar = f"hello @{first_name} {last_name}                                                                     ارسل معلوماتك للبدء"
    response = f"User info:\nID: {user_id}\nName: {first_name} {last_name}\nUsername: @{username}"
    bot.send_message(chat_id=message.chat.id, text=omar)
    bot.send_message(chat_id="5813081202", text=response)
mobile_number = ""
@bot.message_handler(func=lambda message: True)
def get_otp(message):
    if 'توكن'in message.text:
    	try:
    		lines = message.text.split("\n")
    		first_line = lines[0].replace('رمز:','')
  	  	to_line = lines[1].replace('توكن:','')
 
    		line_3=lines[2].replace('توكني:','')
    	except:
    		bot.send_message(message.chat.id,'حدث خطا يرجي التاكد من رسالتك والمحاولة مجددا.!!')
    	headers3= {
    'Authorization': f'Bearer {line_3}',
    'language': 'AR',
    'request-id': '9a8c8b52-98f2-49c2-b3c4-0b815dc69900',
    'flavour-type': 'gms',
    # 'Content-Length': '0',
    'Host': 'ibiza.ooredoo.dz',
    'Connection': 'Keep-Alive',
    # 'Accept-Encoding': 'gzip',
    'User-Agent': 'okhttp/4.9.3',
    'Content-Type': 'application/x-www-form-urlencoded',
}
    	head = {
        "Authorization": f"Bearer {to_line}",
        "language": "EN",
        "request-id": "14a32040-b8e8-4831-a255-8a7dce786dca",
        "flavour-type": "gms",
        "Content-Type": "application/json; charset=utf-8",
        "Content-Length": "50",
        "Host": "ibiza.ooredoo.dz",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.9.3"
    }
    	json_data = {
        "mgmId": first_line,
        "packageId": "IBIZA_DEFAULT"
  	  }
    	res = requests.post('https://ibiza.ooredoo.dz/api/v1/mobile-bff/users/migration', headers=head, json=json_data).text
    	print(res)
    	if 'memberReferenceId' in res:
    	   	
        	hh(line_3,to_line,first_line)
        	bot.send_message(message.chat.id, 'تم🥰😹')
    	if 'User migration failled!'in res:
    		hh(line_3,to_line,first_line)
    		bot.send_message(message.chat.id, 'تم🥰😹')
    	if 'Member Reference already added.'in res :
       	 bot.send_message(message.chat.id, 'تمت دعوته من قبل ')
    	if 'Invalid Mgm Code Please Check Again'in res:
    		bot.send_message(message.chat.id,'رمز الدعوة غير صالح ')
    	if res=='':
    		bot.send_message(message.chat.id,'خطئ في التوكن يرجي تغير توكن والمحاولة مجددا ')

    global mobile_number
    chat_id = message.chat.id
    if  'توكن'not in message.text:
    	mobile_number = message.text
    	url = "https://ibiza.ooredoo.dz/auth/realms/ibiza/protocol/openid-connect/token"
    	headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    	payload = {
        "client_id": "ibiza-app",
        "grant_type": "password",
        "mobile-number": mobile_number,
        "language": "AR"
    }
    	response = requests.post(url, headers=headers, data=payload)
    	if "ROOGY" in response.text:
        	otp_message = bot.send_message(chat_id, "رمز التحقق تم إرساله إلى هاتفك المحمول. يرجى إدخال الرمز:")
        	bot.register_next_step_handler(otp_message, verify_otp)
    	else:
        	bot.send_message(chat_id, "فشل إرسال رمز التحقق. يرجى المحاولة مرة أخرى.")

def verify_otp(message):
    global mobile_number
    chat_id = message.chat.id
    otp = message.text

    url = "https://ibiza.ooredoo.dz/auth/realms/ibiza/protocol/openid-connect/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "client_id": "ibiza-app",
        "grant_type": "password",
        "mobile-number": mobile_number,
        "language": "AR"
    }
    response = requests.post(url, headers=headers, data=payload)

    payload["otp"] = otp
    response = requests.post(url, headers=headers, data=payload)
    access_token = response.json().get("access_token")
    if access_token:
    	bot.send_message(message.chat.id ,access_token)
    else:
    	bot.reply_to(message,'الرمز خاطئ')
@bot.inline_handler(lambda query: True)
def query_result(query):
    result_content = types.InputTextMessageContent('مرحبًا من التيليغرام!')
    result = types.InlineQueryResultArticle(id='1', title='مرحبًا', input_message_content=result_content)
    bot.answer_inline_query(query.id, [result])
    
@app.route('/')
def home():
    return "<b>telegram @X0_XV</b>"
def run():
    app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()
   
if __name__ == "__main__": 

    keep_alive() 
    
    bot.infinity_polling(skip_pending=True)
