#!/usr/bin/env python3

from influxdb import InfluxDBClient
hostip = "127.0.0.1"
hostport = "8086"

client = InfluxDBClient(host=hostip,port=hostport)
def createDatabase():
    print("Creating database")
    client.create_database('database')

client.get_list_database()
client.switch_database('database')
print(client.get_list_database())
json_body = [
    {
        "measurement":"ExcecuteStatus",
        "tags": {
            "user": "koala",
            "programName": "hello.py"
            },
        "fields": {
            "exectime": "1m 52s"
        },
        "measurement":"ExcecuteStatus",
        "tags": {
            "user": "bob",
            "programName": "program.py"
        },
        "fields": {
            "exectime": "20s"
            }
        } 
]

print("Writing to DB")
print(client.write_points(json_body,database='database',protocol=u'json'))
print("Querying data from DB")
print(client.query("SELECT exectime FROM ExcecuteStatus WHERE id='1234'"))
