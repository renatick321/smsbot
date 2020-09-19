import requests


TOKEN = "cf2258772ff94b31f98ecfcd4f362b73"
MAIN_URL = "https://edge.qiwi.com"

NUMBER = '79647833930'

def get_comments(length=15):
	headers = {
		"Accept": "application/json",
		"Content-Type": "application/json",
		"Authorization": "Bearer {}".format(TOKEN)
			  }
	comments = {}
	r = requests.get("https://edge.qiwi.com/payment-history/v2/persons/{}/payments?rows={}".format(NUMBER, length), headers=headers, verify=False).json()
	for i in r["data"]:
	    if i['total']['currency'] == 643:
	        a = "r" if i["comment"] is None else i["comment"]
	        comments[a] = i["sum"]["amount"]
	print(comments)
	return comments