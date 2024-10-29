import requests

BASE_URL = "http://127.0.0.1:8000"

def get_story_price(currency):
    response = requests.get(f"{BASE_URL}/currency",params={'ticker':currency})
    if (response.status_code ==200):
        return response
    else:
        raise Exception(f"Ошибка получения данных{response.text}")
def get_curr_price(currency):
    response = requests.get(f"{BASE_URL}/currency/current",params={'ticker':currency})
    if (response.status_code ==200):
        return response
    else:
        raise Exception(f"Ошибка получения данных{response.text}")

def get_date_price(currency,someDate):
    response = requests.get(f"{BASE_URL}/currency/date",params={'ticker':currency,'date':someDate})
    if (response.status_code ==200):
        return response
    else:
        raise Exception(f"Ошибка получения данных{response.text}")



# get_story_price("BTC")
# get_curr_price("BTC")
# get_date_price("ETH","2024-10-29")