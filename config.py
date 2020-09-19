import random


BOT_TOKEN = "1061151336:AAH-T7q_M-TJfo7UK7JTVDdNNHP-01g_8Nw"
ADMIN = 1198883635

DB_URL = "data/db.db"

CHARS = 'abcdefghijklnopqrstuvwxyz1234567890'
LETTERS = "abcdefghijklnopqrstuvwxyz"


def price_boost(price):
	price = float(price)
	price *= 1.7
	price = float(int(price * 100)) / 100
	return price


def password_create(length=16):
	password = ''
	for i in range(length):
		password += random.choice(CHARS)
	return password