import requests
id = 1
url = f'http://192.168.1.28:8080/json.htm?type=devices&rid={id}'
r =requests.get(url)
data = r.json()

#print(data)

print(data['result'][0]['Data'])
print(data['result'][0]['Name'])
print(data['result'][0]['idx'])