# -*- coding: utf-8 -*-
import time
import telebot
import pyowm
import random
from telebot import apihelper
from telebot import types
import sqlite3

apihelper.proxy = {'https': 'socks5://mazafaka:mazafaka123@178.128.24.1:1080'}
owm = pyowm.OWM('14baa3aa4e4af1c7f7af28efb77b7934',language = "ru")
bot = telebot.TeleBot('976683817:AAGsJ8-PzmOjte0-Tmo1t2ydces4hLVLb_g')
search = '' 

@bot.message_handler(commands=['start'])

def start_message(message):
	bot.send_message(message.from_user.id,"Привет")
	bot.send_message(message.from_user.id, "Вот что я могу :",reply_markup = keyboard())

@bot.message_handler(content_types=['text'])
def obs(message):
	if message.text == "🌡Погода🌡":
		bot.send_message(message.from_user.id, "погода в каком городе тебя интересует ?")
		bot.register_next_step_handler(message, get_sity)

	elif message.text =="😸МеМ😸":
		rand = random.randint(1,10)
		memas = { 1 : 'C:/python_telega_bot/mems/K9KncxcD0y4.jpg',
				  2 : 'C:/python_telega_bot/mems/WLyoRC6NBHg.jpg', 
				  3 : 'C:/python_telega_bot/mems/images.jpg',
				  4 : 'C:/python_telega_bot/mems/images (2).jpg',
				  5 : 'C:/python_telega_bot/mems/images (1).jpg', 
				  6 : 'C:/python_telega_bot/mems/Dknnxv5JadA.jpg',
				  7 : 'C:/python_telega_bot/mems/best-grumpy-cat-memes-4.jpg',
				  8 : 'C:/python_telega_bot/mems/b_w1lpEeyTo.jpg', 
				  9 : 'C:/python_telega_bot/mems/69101490_2485848461644262_7002191598550888784_n.jpg',
				  10 : 'C:/python_telega_bot/mems/MqvF9m1vPYs.jpg',
				   
		}
		bot.send_photo(message.from_user.id, open(memas[rand], 'rb'))
		bot.send_message(message.from_user.id, "",reply_markup = keyboard())

	elif message.text =="/reg":
		bot.send_message(message.from_user.id, "вход в аккаунт администратора")
		bot.send_message(message.from_user.id, "введите логин:")
		bot.register_next_step_handler(message, get_login)


def get_login(message):
	conn = sqlite3.connect("TelegaUsInf.db") #вход в бд
	cursor = conn.cursor()
	if (message.text == 'admin'): #*инфа из DB*
		bot.send_message(message.from_user.id, "введите пароль:")
		if  (message.text == 'admin'):
			print("cool")
		else:
			bot.send_message(message.from_user.id, "пароль неверный")
			print ("necool")

	else:
		bot.send_message(message.from_user.id, "логин неверный")
		print(message.text.title())


def get_sity(message):
	try:	
		observation = owm.weather_at_place(message.text.title())
		w = observation.get_weather()
		stat = w.get_detailed_status()
		temp = w.get_temperature('celsius')["temp"]
		answer = "в этом городе сейчас  : {0}  \n\nтемпература : {1}".format(stat,temp)
		bot.send_message(message.chat.id,answer,reply_markup = keyboard())
		global search 
		search = message.text.title()
		print (search)
		a = time.ctime(time.time())
		print(a)
	



		print(message.from_user.id)
		name = message.from_user.first_name


		conn = sqlite3.connect('TelegaUsInf.db')
		c = conn.cursor()
		######c.execute('''CREATE TABLE users_info (id integer  primary key autoincrement, timer text not null ,name text not null, search text not null )''')

		c.execute("INSERT INTO users_info (timer,name,search) VALUES ('{0}','{1}','{2}')".format(a,name,search))

		conn.commit()
		c.close()
		conn.close()

	except pyowm.exceptions.api_response_error.NotFoundError:
		bot.send_message(message.from_user.id,"Неверно указан населенный пункт")




def keyboard():
	markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True)
	btn1 = types.KeyboardButton('🌡Погода🌡')
	btn2 = types.KeyboardButton('😸МеМ😸')
	markup.add(btn1,btn2)
	return markup

bot.polling( none_stop = True ) 