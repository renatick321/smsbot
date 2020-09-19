import requests 
import random
from time import sleep


APIKEY = '39795U36a7fd4ecb1ca5f4ab5b074049c5f101'
SERVICE = 'qw'
OPERATOR = None
BAD = 8
GOOD = 6

smshub = {
    "Telegram": "tg",
    "Вконтакте": "vk",
    "Whatsapp": "wa",
    "Avito": "av",
    "Qiwi": "qw",
    "Пятерочка": "bd",
    "DeliveryClub": "dt",
    "Mail.ru": "ma",
    "Burger King": "ip",
    "Яндекс": "ya",
    "Юла": "ym",
    "Instagram": "ig",
    "Google": "go",
    "Ok.ru": "ok",
         }

COUNTRY = {
	"Россия": 0,
	"Украина": 1,
	"Казахстан": 2 
		  }
#  Сразу после получения номера доступны следующие действия:
#  8 - Отменить активацию
#  1 - Сообщить, что SMS отправлена (необязательно)
#  Для активации со статусом 1:
#  8 - Отменить активацию
# ==========================================================
#  Сразу после получения кода:
#  3 - Запросить еще одну смс
#  6 - Подтвердить SMS-код и завершить активацию
#  Для активации со статусом 3:
#  6 - Подтвердить SMS-код и завершить активацию
def info():
	l = [
	' Сразу после получения номера доступны следующие действия:',
	' 8 - Отменить активацию',
	' 1 - Сообщить, что SMS отправлена (необязательно)',
	' Для активации со статусом 1:',
	' 8 - Отменить активацию',
	'==========================================================',
	' Сразу после получения кода:',
	' 3 - Запросить еще одну смс',
	' 6 - Подтвердить SMS-код и завершить активацию',
	' Для активации со статусом 3:',
	' 6 - Подтвердить SMS-код и завершить активацию'
		]
	print("\n".join(l))

def price_boost(price):
    print(price)
    price = float(price)
    price *= 1.2
    price = float(int(price * 100)) / 100
    print(price)
    return price

def get_price(service, country, apikey=APIKEY):
	r = requests.get("https://smshub.org/stubs/handler_api.php?api_key={}&action=getPrices&service={}&country={}".format(APIKEY, service, COUNTRY[country]))
	d = r.json()
	key = list(dict(d).keys())[0]
	try:
		print(key)
		a = d[key][service]
		lst = sorted(a)[0]
		price = str(price_boost(str(lst))) + ' ₽'
	except:
		price = 'Нет в наличии'
	return price

class Number:
	def __init__(self, service, country, apikey=APIKEY):
		self.country = COUNTRY[country]
		self.service = service
		self.apikey = apikey
		try:
			url = "https://smshub.org/stubs/handler_api.php?api_key={}&action=getNumber&service={}&country={}".format(self.apikey, self.service, self.country)
			r = requests.get(url).text
			b = False if r == 'NO_NUMBERS' or r == 'NO_BALANCE' else True
			s, self.id, self.number = map(str, r.split(":"))
		except:
			self.number = ""

	def __str__(self):
		return str(self.number)

	def get_sms(self, queue):
		for i in range(240):
			sleep(1)
			r = requests.get("https://smshub.org/stubs/handler_api.php?api_key={}&action=getStatus&id={}".format(self.apikey, self.id)).text
			print(r)
			if "STATUS_OK" in r:
				queue.put(r[len("STATUS_OK:"):])
				break
			elif "STATUS_CANCEL" == r:
				queue.put("Аренда номера была отменена")
				break
		queue.put("Аренда номера была отменена")

	def edit_status(self, status):
		r = requests.get("https://smshub.org/stubs/handler_api.php?api_key={}&action=setStatus&status={}&id={}".format(self.apikey, status, self.id))
		return r.text

	def get_balance(self):
		r = requests.get("https://smshub.org/stubs/handler_api.php?api_key={}&action=getBalance".format(self.apikey))
		return r.text
