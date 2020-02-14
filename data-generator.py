import threading
import requests, json
import random

url = 'http://127.0.0.1:5000/test/1234'

data = [
    [ 0, 500, 0],
    [ 0, 502, 0],
    [ 0, 504, 0],
    [ 0, 505, 0],
    [ 0, 510, 0],
    [ 0, 510, 0],
    [ 0, 510, 0]
]

def sendData():
    print(data)


    for i in range(1, 6):
      data[i-1] = data[i]

    data[6][1] = data[6][1] + random.uniform(-1, 5)
    

    response = requests.post(url, headers = {'Content-Type': 'application/json; charset=utf-8'} , data=json.dumps({'data':data}))
    

def setInterval(func,time):
    e = threading.Event()
    while not e.wait(time):
        func()



setInterval(sendData, 3)