import requests
import os
import json
import datetime
import pytz
import pandas as pd
import random


blackListOfCtypto = ['PEPE']

TelegramBotToken = '6332232715:AAGokeIY5X06lGY1wDQKQPrFi6Rma8UgGKs'
myUserId = '6283830983'
Group0Id = '-1001914019896'

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
            json.dump(data, file)  # Write data to file in JSON format
    else:
        #print("Le fichier existe déjà. Attendre la prochaine heure.")
        pass

def getData():
    createData()
    dataCGfilePath = getDataPath()
    with open(dataCGfilePath, 'r') as file:
        data = json.load(file)  # Load data from the file as a JSON object
    return data

def rqCG150CryptoSymbMC():
    data = getData()

    list150Crypto = []
    list150Symbol = []
    for crypto in data:
        list150Crypto.append(crypto['name'].lower())
        list150Symbol.append(crypto['symbol'])


    for all in blackListOfCtypto:
        all = all.lower()
        if all in list150Crypto:
            index = list150Crypto.index(all)
            list150Crypto.remove(all)
            list150Symbol.pop(index)

        if all in list150Symbol:
            index = list150Symbol.index(all)
            list150Symbol.remove(all)
            list150Crypto.pop(index)
    return list150Crypto,list150Symbol

def get_crypto_price(crypto_symbol):
    
    data = getData()

    if isinstance(crypto_symbol, str):
        crypto_symbol = crypto_symbol.lower()
        for index, crypto in enumerate(data):
            name = crypto.get("name", "").lower()
            symbol = crypto.get("symbol", "").lower()
            #print(name,symbol,":",crypto_symbol)

            if crypto_symbol == name or crypto_symbol == symbol:
                price = crypto.get("current_price")
                return price
        return 'error'
    
    elif isinstance(crypto_symbol, list):
        msg = ""
        for Sym in crypto_symbol:
            Sym = str(Sym).lower()
            if (Sym == 'polygon'):
                Sym = 'matic'

            for index, crypto in enumerate(data):
                name = crypto.get("name", "").lower()
                symbol = crypto.get("symbol", "").lower()

                if Sym == name or Sym == symbol:
                    price = crypto.get("current_price")
                    rate = get_exchange_rate(symbol)
                    msg += f"${name.capitalize()}: ${price}, 24H: {rate}\n"      
        return msg
    
    else:
        msg = ""
        for i, crypto in enumerate(data):
            if i == 10:
                break
            name = crypto.get("name", "")
            symbol = crypto.get("symbol", "").lower()
            market_cap = crypto.get("current_price", "")
            rate = get_exchange_rate(symbol)
            msg += f"${name}: ${market_cap}, 24H: {rate}\n"
        return msg

def get_exchange_rate(crypto_symbol='', currency='usd'):
    data = getData()

    if crypto_symbol:
        crypto_symbol = crypto_symbol.lower()
        for index, crypto in enumerate(data):
            name = crypto.get("name", "").lower()
            symbol = crypto.get("symbol", "").lower()

            if crypto_symbol == name or crypto_symbol == symbol:
                change24 = round(crypto.get("price_change_percentage_24h"),2)
                change24 = str(change24) + '%'
                return change24
        return 'error'
    else:
        dictRate= {}
        for i, crypto in enumerate(data):
            if i == 10:
                break
            name = crypto.get("name", "")
            if name =='Tether' or name =='USD Coin' or name =='Dai':
                continue
            change24 = round(crypto.get("price_change_percentage_24h", ""),2)
            dictRate[name] = change24
        sortedDict = dict(sorted(dictRate.items(), key=lambda x: x[1], reverse=True))
        top_5_rates = list(sortedDict.items())[:5]
        msgRate = '\n'.join([f"${pair[0]}: {pair[1]}%" for pair in top_5_rates])
        return msgRate

def listToDictCounter(symbolList):
    symbolDict = {}
    for symbol in symbolList:
        symbol = symbol.upper()
        if symbol in symbolDict:
            symbolDict[symbol] += 1
        else:
            symbolDict[symbol] = 1
    return symbolDict

def telegramBotSendtextGroup(message):
   
   send_text = 'https://api.telegram.org/bot' + TelegramBotToken + '/sendMessage?chat_id=' + Group0Id + '&parse_mode=Markdown&text=' + message

   response = requests.get(send_text)

   return response.json()

def persoTelegramBot(message):
       
   send_text = 'https://api.telegram.org/bot' + TelegramBotToken + '/sendMessage?chat_id=' + myUserId + '&parse_mode=Markdown&text=' + message

   response = requests.get(send_text)

   return response.json()

def get_info_GSheet():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRubjP6w-B_f48XgoW-4NLOSkmPtJNwi8bXmvDPvUZ_GuoCdxV88ET6YPVvVczjQxjF3BCqDYqRxDoq/pub?gid=0&single=true&output=csv"

    df = pd.read_csv(url,sep=',',decimal='.')
    df = df.dropna(how='all')
    range_values = int(df["Name"].nunique())

    msg =""
    totalPrice = 0
    for x in range(range_values):
        cell_Name = df.loc[x,"Name"]
        row_index = df[df["Name"] == cell_Name].index.item()

        if not pd.isna(row_index):
            cellValue = df.loc[row_index, "Quantity"]
            if cellValue == 'Chargement en cours ...':
                price = df.loc[row_index,"Value"]
            else:
                cellValue = cellValue.replace(',','.')
                #print(cell_Name)
                price = float(get_crypto_price(cell_Name.lower()))
                price *= round(float(cellValue),6)
                totalPrice += price
                rate = get_exchange_rate(cell_Name)

            msg += f"{cellValue} {cell_Name} = {round(price,3)}$ 24h: {rate}\n"
        else:
            msg += f"{cell_Name} error"
    msg = f'Total {round(totalPrice,2)}$ \n' + msg
    return msg

def pileFace():
    k = random.randint(0,1)
    if (k == 0):
        return "Pile"
    else:
        return "Face"
