import requests

ip = '192.168.1.28'
port = '8080'

def switchLight(id=1,status='Off'):
    url = f'http://{ip}:{port}/json.htm?type=command&param=switchlight&idx={id}&switchcmd={status}'
    try:
        r =requests.get(url)
    except:
        msg = "probleme switchlight avec la requete verifier l'url"
        return msg
    else:
        msg = getStatusDomo(id)
    
    return msg

def getStatusDomo(id=1):
    url = f'http://{ip}:{port}/json.htm?type=devices&rid={id}'
    try:
        r =requests.get(url)
    except:
        msg = "probleme getStatus avec la requete verifier l'url"
        return msg
    else:
        data = r.json()
        status = data['result'][0]['Data']
        name = data['result'][0]['Name']

        msg = f'{name} is {status}'

    return msg

def getListDomo():
    switch = {}
    url = f"http://{ip}:{port}/json.htm?type=command&param=getlightswitches"
    try:
        r =requests.get(url)
    except:
        msg = "probleme getlist avec la requete verifier l'url"
        return msg
    else:
        data = r.json()
        msg = ""

        for x in range(len(data['result'])):
            name = data['result'][x]['Name']
            switch[name] = int(data['result'][x]['idx'])
            
        switch = dict(sorted(switch.items(), key=lambda item: item[1]))
        list_keys = list(switch.keys())
        for x in range(len(list_keys)):
            msg += f"{list_keys[x]} a pour id {switch[list_keys[x]]}\n"

    return msg

