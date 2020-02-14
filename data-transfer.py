import threading
import requests, json
import random

url = 'http://203.247.166.20:5000/data-transfr/1234'

data = {
    'temp' : [687.0, 778.4, 865.4 , 930.2, 992.7, 996.1, 1010.2 , 1008.0, 1019.6 ,1019.1],
    'gas' : [2.3,8,3.4,1.2,2.3,4.5,2.3,1.6,2.4,5],
    'weight' : [52300],
    'work' : [20191001]
}

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