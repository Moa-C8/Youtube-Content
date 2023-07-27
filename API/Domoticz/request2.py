import requests

id = 1
status = 'Off'

url = f'http://192.168.1.28:8080/json.htm?type=command&param=switchlight&idx={id}&switchcmd={status}'
r =requests.get(url)
