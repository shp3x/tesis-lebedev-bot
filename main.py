# -*- coding: utf-8 -*-
# created by Shpex
import sqlite3
import telebot
import requests
import time
import io
import os
import datetime
import threading
import PIL
import config

from telebot import types
from io import BytesIO
from PIL import Image
from datetime import date
from config import API_TOKEN, ADMIN_USERNAME

bot = telebot.TeleBot(API_TOKEN) #Берет данные из config.py
admin = (ADMIN_USERNAME) #Берет данные из config.py

print("Бот запущен!")

# Коннектимся к базе данных
conn = sqlite3.connect('tesis.db', check_same_thread=False)
cursor = conn.cursor()

def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
	cursor.execute('INSERT OR IGNORE INTO main (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)', (user_id, user_name, user_surname, username))
	conn.commit()

@bot.message_handler(commands=['start'])
def start(message):
    us_id=message.from_user.id
    us_name=message.from_user.first_name
    us_sname=message.from_user.last_name
    username=message.from_user.username
    
    db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)

# Создаем кнопку 'Начать'
    nachat = types.ReplyKeyboardMarkup(resize_keyboard=True)
    nachatbtn = types.KeyboardButton('Начать')

# Добавляем кнопку 'Начать'
    nachat.add(nachatbtn)

# Бот уже добавил пользователя в БД, отправляем приветственное сообщение
    bot.send_message(message.chat.id, 'Приветствую!\n\nЧтобы начать пользоваться ботом - нажмите кнопку Начать', reply_markup=nachat)

@bot.message_handler(commands=['contact'])
def start(message):
    bot.send_message(message.chat.id, 'Связь с администратором', parse_mode='Markdown') 
    bot.send_message(message.chat.id, ADMIN_USERNAME, parse_mode='Markdown')

@bot.message_handler(content_types=['text'])
def now(message):
    if message.text == 'Начать':

    #Создаем кнопки 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itembtna = types.KeyboardButton('Магнитные бури')
        itembtnb = types.KeyboardButton('Прогноз магнитных бурь')
        itembtnc = types.KeyboardButton('Индекс вспышечной активности')
        itembtnd = types.KeyboardButton('График вспышечной активности')

    #Добавляем кнопки 
        markup.add(itembtna)
        markup.add(itembtnb)
        markup.add(itembtnc)
        markup.add(itembtnd)
        
        bot.send_photo(message.chat.id, photo=open('img/logo.png', 'rb')) #Отправляем логотип
        bot.send_message(message.chat.id, '*Бот готов к использованию!*', reply_markup=markup, parse_mode='Markdown')

    if message.text == 'Магнитные бури':

        now = Image.new("RGBA", (700, 400), (0, 0, 0)) #Создаем фон черного цвета 700x400px
        response_now = requests.get('https://tesis.lebedev.ru/upload_test/files/kp.png') #Берем PNG изображение с сайта
        now_img = Image.open(BytesIO(response_now.content)).convert("RGBA")
        x_now, y_now = now_img.size
        now.paste(now_img, (0, 0, x_now, y_now), now_img) #Накладываем слой с основным изображением на слой с фоном
        now.save("img/now/now.png", format="png") #Сохраняем результат в папку

        bot.send_photo(message.chat.id, photo=open('img/now/now.png', 'rb'), caption='*Магнитные бури за последние три дня*', parse_mode= "Markdown") #Отправляем результат юзеру
        #os.remove("now/now.png") Команда удаляет изображение
    elif message.text == 'Прогноз магнитных бурь':

        prognoz = Image.new("RGBA", (725, 400), (0, 0, 0))
        response_prognoz = requests.get('https://tesis.lebedev.ru/upload_test/files/fc3.png')
        prognoz_img = Image.open(BytesIO(response_prognoz.content)).convert("RGBA")
        x_prognoz, y_prognoz = prognoz_img.size
        prognoz.paste(prognoz_img, (0, 0, x_prognoz, y_prognoz), prognoz_img)
        prognoz.save("img/prognoz/prognoz.png", format="png")
        
        bot.send_photo(message.chat.id, photo=open('img/prognoz/prognoz.png', 'rb'), caption='*Прогноз магнитных бурь на три дня*', parse_mode= "Markdown")
        #os.remove("prognoz/prognoz.png") команда удаляет изображение после отправки
    elif message.text == 'Индекс вспышечной активности':

        flash = Image.new("RGBA", (700, 100), (0, 0, 0))
        response_flash = requests.get('https://tesis.lebedev.ru/upload_test/files/informer.png')
        flash_img = Image.open(BytesIO(response_flash.content)).convert("RGBA")
        x_flash, y_flash = flash_img.size
        flash.paste(flash_img, (0, 0, x_flash, y_flash), flash_img)
        flash.save("img/flash/flash.png", format="png")

        bot.send_photo(message.chat.id, photo=open('img/flash/flash.png', 'rb'), caption='*Индекс вспышечной активности*', parse_mode= "Markdown")
        #os.remove("flash/flash.png") команда удаляет изображение после отправки        
    elif message.text == "График вспышечной активности":

        grafik = Image.new("RGBA", (751, 471), (0, 0, 0))
        response_grafik = requests.get('https://tesis.lebedev.ru/upload_test/files/flares_REL0.png')
        grafik_img = Image.open(BytesIO(response_grafik.content)).convert("RGBA")
        x_grafik, y_grafik = grafik_img.size
        grafik.paste(grafik_img, (0, 0, x_grafik, y_grafik), grafik_img)
        grafik.save("img/grafik/grafik.png", format="png")

        bot.send_photo(message.chat.id, photo=open('img/grafik/grafik.png', 'rb'), caption='*График вспышечной активности*', parse_mode= "Markdown")
        #os.remove("grafik/grafik.png") команда удаляет изображение после отправки   

bot.infinity_polling()