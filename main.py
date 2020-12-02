#!/usr/bin/env python3

from influxdb import InfluxDBClient
import time
import subprocess
import sys
hostip = "docker.therepairbear.koala"
hostport = "8086"

client = InfluxDBClient(host=hostip,port=hostport)
def createDatabase():
    print("Creating database")
    client.create_database('ExecStats')

#createDatabase()
#client.drop_database('ExecStats')
client.get_list_database()
client.switch_database('ExecStats')
print(client.get_list_database())

currtime = float(time.time())
print(currtime)
print("Starting program now")

process = subprocess.run(["python3","part2.py"])
subprocess.CompletedProcess.check_returncode(process)

print("Program has finished")
currendtime = float(time.time())

json_body = [
    {
        "measurement":"ExcecuteStatus",
        "tags": {
            "username": "bob",
            "programName": "program3.py"
            },
        "fields": {
            "startTime": currtime,
            "endtime": currendtime 
            }
    } 
]

print("Writing to DB")
client.write_points(json_body,database='ExecStats',protocol=u'json')
print("Querying data from DB")
#client.drop_database('database')
#print(client.query("SELECT exectime FROM ExecStats.autogen.ExcecuteStatus WHERE \"username\"='koala' AND programName='hello.py' FILL(null)"))
