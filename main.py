#!/usr/bin/env python3

from influxdb import InfluxDBClient
hostip = "docker.therepairbear.koala"
hostport = "8086"

client = InfluxDBClient(host=hostip,port=hostport)
def createDatabase():
    print("Creating database")
    client.create_database('ExecStats')

#createDatabase()
client.get_list_database()
client.switch_database('ExecStats')
print(client.get_list_database())
json_body = [
    {
        "measurement":"ExcecuteStatus",
        "tags": {
            "username": "koala",
            "programName": "hello.py"
            },
        "fields": {
            "exectime": "1m 52s"
        }
    } 
]

print("Writing to DB")
print(client.write_points(json_body,database='ExecStats',protocol=u'json'))
print("Querying data from DB")
client.drop_database('database')
print(client.query("SELECT exectime FROM ExecStats.autogen.ExcecuteStatus WHERE \"username\"='koala' FILL(null)"))
