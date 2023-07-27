import json

with open('data.txt','r') as file:
    data = json.load(file)

print(data[1]['current_price'],'$')