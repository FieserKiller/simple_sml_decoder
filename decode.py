import requests
import time
import datetime

url = 'http://tibber-host/data.json?node_id=1'
user = 'admin'
password = 'XXXX-XXXX'

data = None
prev_moment = 0
prev_total = 0
while True:
    response = requests.get(url, auth=(user, password))
    data = response.content
    searchTotal = b'\x77\x07\x01\x00\x01\x08\x00\xff\x64'
    pos = data.find(searchTotal)
    total_int = 0
    if (pos != -1):
        pos = pos + len(searchTotal) + 9
        total = data[pos:pos + 8]
        total_int = int.from_bytes(total, "big")

    searchMoment = b'\x77\x07\x01\x00\x10\x07\x00\xff\x01\x01\x62\x1b\x52\xfe\x59'
    pos = data.find(searchMoment)
    moment_int = 0
    if (pos != -1):
        pos = pos + len(searchMoment)
        moment = data[pos:pos + 8]
        moment_int = int.from_bytes(moment, "big")

    if (total_int == 0 or moment_int == 0):
        print(str(datetime.datetime.now())+': Malformed data found:'+str(len(data))+' :'+str(data))
        
    elif (total_int != prev_total or moment_int != prev_moment):
        print(str(datetime.datetime.now())+' Total: ' + str(total_int)+' Moment:'+str(moment_int))
        prev_moment = moment_int
        prev_total = total_int
    time.sleep(2)
