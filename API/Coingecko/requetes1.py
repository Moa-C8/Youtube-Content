import requests

url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
            "vs_currency": "usd",
            "per_page": 200,
        }
req = requests.get(url, params=params)
data = req.json()

with open('data.txt','w') as file:
    file.write(str(data))