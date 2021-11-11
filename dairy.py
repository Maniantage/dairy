import os
import datetime
from bs4 import BeautifulSoup
import telebot
from telebot import types
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

limit = 7

options = Options()
binary = r'/usr/bin/firefox'
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream,application/vnd.ms-excel")
options.binary = binary
options.headless = True
date = datetime.datetime.today()
bot = telebot.TeleBot('2113663446:AAFIJSyqzowXx-8KpujCAfWlB3k2HjnVWK4')

def dow(date):
    days=['Понедельник','Вторник','Среда','Четверг','Пятница','Субота','Воскресенье']
    dayNumber=date.weekday()
    return days[dayNumber]

def browser_window(browser):
    browser.execute_script('window.open()')
    browser.switch_to.window(browser.window_handles[0])
    browser.close()
    browser.switch_to.window(browser.window_handles[0])

def get_s_write(date, browser):
    if dow(date) != 'Субота' or 'Воскресенье':
        subjects = []
        browser.get('http://schedule.in.ua/dashboard/vische-profesiine-uchilische-7/group/612d20eead96a3fb6ed3eccf')
        source_data = browser.page_source
        soup = BeautifulSoup(source_data, 'html.parser')
        lessons = soup.find_all('div', 'item ng-star-inserted')
        for index, x in enumerate(lessons):
            num = x.text[0]
            cabinet = x.text[1:].rsplit('.', 2)[-1]
            only_lesson = x.text[1:].rsplit('.', 2)[0].rsplit(' ', 3)[0]
            if 'Іноземна мова' in only_lesson:
                only_lesson = x.text[1:].split('2', 1)[0]
                cabinet = x.text[1:].rsplit(' ', 5)[1]  
            subjects.append('Урок ' + num + ' → ')
            subjects.append(only_lesson + '│')
            subjects.append(' Кабинет: ' + cabinet + '\n')
            if index == limit:
                break
        browser_window(browser)
    else:
        return 'Иди поспи сегодня выходной'
    return subjects



@bot.message_handler(commands=['start'])
def menu(message):
    start_menu = types.ReplyKeyboardMarkup(True, True)
    start_menu.row('Расписание')
    bot.send_message(message.chat.id, 'Стартовое меню', reply_markup=start_menu)
    
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Расписание':
        subjects = get_s_write(date, browser)
        if len(subjects) == 0:
            bot.send_message(message.chat.id, 'Упс.. что то пошло не так, попробуйте еще раз', subjects, reply_markup=menu(message))
        else:
            finish = "".join(map(str, subjects))
            bot.send_message(message.chat.id, 'Расписание на сегодня \n' + str(finish), reply_markup=menu(message))
    else:
        bot.send_message(message.chat.id, 'Нет такой команды. Поробуйте /start')

if __name__ == '__main__':
    browser = webdriver.Firefox(options = options, executable_path='/usr/local/bin/geckodriver.exe')
    browser.set_window_size(765, 937)
    bot.infinity_polling()

    
    
