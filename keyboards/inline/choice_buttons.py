from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import buy_callback


def num():
    keyboard = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('Telegram', callback_data='Telegram')
    btn2 = InlineKeyboardButton('Whatsapp', callback_data='Whatsapp')
    keyboard.row(btn1, btn2)
    btn1 = InlineKeyboardButton('Вконтакте', callback_data='Вконтакте')
    btn2 = InlineKeyboardButton('Avito', callback_data='Avito')
    keyboard.row(btn1, btn2)
    btn1 = InlineKeyboardButton('Qiwi', callback_data='Qiwi')
    btn2 = InlineKeyboardButton('Пятерочка', callback_data='Пятерочка')
    keyboard.row(btn1, btn2)
    btn1 = InlineKeyboardButton('Mail.ru', callback_data='Mail.ru')
    btn2 = InlineKeyboardButton('Delivery Club', callback_data='DeliveryClub')
    keyboard.row(btn1, btn2)
    btn1 = InlineKeyboardButton('Burger King', callback_data='Burger King')
    btn2 = InlineKeyboardButton('Яндекс', callback_data='Яндекс')
    keyboard.row(btn1, btn2)
    btn1 = InlineKeyboardButton('Юла', callback_data='Юла')
    btn2 = InlineKeyboardButton('Instagram', callback_data='Instagram')
    keyboard.row(btn1, btn2)
    btn1 = InlineKeyboardButton('Google', callback_data='Google')
    btn2 = InlineKeyboardButton('Ok.ru', callback_data='Ok.ru')
    keyboard.row(btn1, btn2)
    keyboard.row(InlineKeyboardButton('↪ В главное меню ↩', callback_data='В главное меню'))
    return keyboard


def cash_check(comment):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("Проверить оплату", callback_data=comment))
    return keyboard


def number_end():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("⛔ Закончить", callback_data='Закончить'))
    return keyboard

def number_sms():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("✉ Ещё смс", callback_data='Ещё смс'))
    keyboard.row(InlineKeyboardButton("⛔ Закончить", callback_data='Закончить'))
    return keyboard

def end_sms():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("❌ Отменить", callback_data='Отменить'))
    return keyboard


def country_btns(lib, services, choice):
    keyboard = InlineKeyboardMarkup()
    ru = lib.get_price(services[choice], "Россия")
    ua = lib.get_price(services[choice], "Украина")
    kz = lib.get_price(services[choice], "Казахстан")
    keyboard.row(InlineKeyboardButton("🇷🇺 Россия | {}".format(ru), callback_data='Россия'))
    keyboard.row(InlineKeyboardButton("🇺🇦 Украина | {}".format(ua), callback_data='Украина'))
    keyboard.row(InlineKeyboardButton("🇰🇿 Казахстан | {}".format(kz), callback_data='Казахстан'))
    return keyboard

def web():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("🔥 Дешёвые 🔥", callback_data='sms-hub'))
    keyboard.row(InlineKeyboardButton("✅ Проверенные ✅", callback_data='sms-activate'))
    #keyboard.row(InlineKeyboardButton("sms-online", callback_data='sms-online'))
    return keyboard