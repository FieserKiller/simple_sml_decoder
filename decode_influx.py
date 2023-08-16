import requests
import time
import datetime
import influxdb_client
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import Point
import systemd_watchdog

url = 'http://tibber-host/data.json?node_id=1'
user = 'admin'
password = 'XXXX-XXXX'
influx_url = 'http://10.9.8.1:8086'
influx_user = 'tibberPulse'
influx_password = 'tibberPulse'
influx_bucket = 'tibberPulse'

wd = systemd_watchdog.watchdog()
wd.ready()
influx_client = InfluxDBClient(url=influx_url,token=f'{influx_user}:{influx_password}',org="-")
influx_write_api = influx_client.write_api(write_options=SYNCHRONOUS)
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
        print(str(datetime.datetime.now())+': Malformed data found:'+str(len(data)))
        
    elif (total_int != prev_total or moment_int != prev_moment):
        #print("total:"+str(total_int)+" moment:"+str(moment_int))
        p = Point("tibber").field("total", total_int).field("moment", moment_int)
        influx_write_api.write(bucket=influx_bucket, record=p)
        prev_moment = moment_int
        prev_total = total_int
    
    if wd.is_enabled:
        wd.ping()
    time.sleep(2)
