#!/usr/bin/env python3

from influxdb import InfluxDBClient
import time
import subprocess
import sys
import os
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for
hostip = "docker.therepairbear.koala"
hostport = "8086"

client = InfluxDBClient(host=hostip,port=hostport)
def createDatabase():
    print("Creating database")
    client.create_database('ExecStats')

#createDatabase()
#client.drop_database('ExecStats')
#print(client.get_list_database())


client.get_list_database()
client.switch_database('ExecStats')
app = Flask(__name__)
UPLOAD_FOLDER= '/home/koala/programming/ExecuteStats'
ALLOWED_EXTENSIONS = {'txt','py','lua'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=["GET","POST"])

def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
        file = request.files['file']
#        if 'user' not in request.:
#            print("no user")
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if request.authorization == None:
            return("\n No user selected, select a username using -u \n ")
        if file and allowed_file(file.filename) and request.authorization != None:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(request.authorization)
            username = request.authorization["username"]
            writetodatabase(filename,username)
            return("")
def writetodatabase(filename,username):
    currtime = float(time.time())
    print(currtime)

    print("Starting program now")

    process = subprocess.run(["python3",filename])
    subprocess.CompletedProcess.check_returncode(process)

    print("Program has finished")
    currendtime = float(time.time())

    json_body = [
        {
            "measurement":"ExcecuteStatus",
            "tags": {
                "username": username,
                "programName": filename
                },
            "fields": {
                "startTime": currtime,
                "endtime": currendtime 
                }
        } 
    ]

    print("Writing to DB")
    client.write_points(json_body,database='ExecStats',protocol=u'json')

app.run()



