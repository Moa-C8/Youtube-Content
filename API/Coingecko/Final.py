import requests
import os
import json
import datetime

def getDataPath():
    today = datetime.datetime.now()
    dat = today.strftime("%Y-%m-%d-%H")
    dataCGfilePath = f"data/{dat}.txt"
    return dataCGfilePath

def createData():
    dataCGfilePath = getDataPath()
    if not os.path.exists(dataCGfilePath):
        os.makedirs(os.path.dirname(dataCGfilePath), exist_ok=True)

        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "per_page": 200,
        }
        req = requests.get(url, params=params)
        data = req.json()

        with open(dataCGfilePath, 'w+') as file:
            json.dump(data, file)
    else:
        print("Le fichier existe déjà. Attendre la prochaine heure.")
        pass

def getData():
    createData()
    dataCGfilePath = getDataPath()
    with open(dataCGfilePath, 'r') as file:
        data = json.load(file)
    return data

data = getData()