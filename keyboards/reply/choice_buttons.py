from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def remove_keyboard():
	keyboard = ReplyKeyboardRemove()
	return keyboard


def menu():
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	keyboard.row(KeyboardButton('🔥 Номера'), KeyboardButton("🆘 Правила"), KeyboardButton("💰 Баланс"))
	keyboard.row(KeyboardButton('💩 Помощь'), KeyboardButton("💼 Мой профиль"))
	return keyboard


def method_payment():
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	keyboard.row(KeyboardButton("🥝 Киви"))
	keyboard.row(KeyboardButton("↪ В главное меню ↩"))
	return keyboard


def balance():
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	keyboard.row(KeyboardButton('🎁 Купон 🎁'), KeyboardButton("💣 Пополнить 💣"))
	keyboard.row(KeyboardButton('↪ В главное меню ↩'))
	return keyboard


def tomenu():
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	keyboard.row(KeyboardButton("↪ В главное меню ↩"))
	return keyboard