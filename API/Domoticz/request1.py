import requests

url = "http://192.168.1.28:8080/json.htm?type=command&param=getlightswitches"
req = requests.get(url)
data = req.json()

with open('data.txt','w') as file:
    file.write(str(data))