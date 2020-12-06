#!/usr/bin/env python3

from influxdb import InfluxDBClient
import time
import subprocess
import sys
import os
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for, jsonify
import json
import bcrypt
import sqlite3
hostip = "docker.therepairbear.koala"
hostport = "8086"
#sqlite3.createDatabase('database.db')
conn = sqlite3.connect('database.db')
c = conn.cursor()
client = InfluxDBClient(host=hostip,port=hostport)
def createDatabase():
    print("Creating database")
    client.create_database('ExecStats')

client.get_list_database()
client.switch_database('ExecStats')


app = Flask(__name__)
app.config['SECRET_KEY'] = '&RUS7vHsmj8Sa!8EWF'
app.debug = True

UPLOAD_FOLDER= '/home/koala/programming/python/ExecuteStats'
ALLOWED_EXTENSIONS = {'txt','py','lua'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=["GET","POST"])
def upload_file():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    cursor = c.execute("SELECT username,password FROM users")
    RequestUsername = request.authorization["username"].encode("utf-8")
    RequestPassword = request.authorization["password"].encode("utf-8")
    for row in cursor:
        hashedpasswd = row[1] 
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return("")
        file = request.files['file']
        if not request.authorization["username"]:
            print("no user")
            return("No user")
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if request.authorization == None:
            return("\n No user selected, select a username using -u \n ")
        if file and allowed_file(file.filename) and bcrypt.checkpw(RequestPassword, hashedpasswd):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            writetodatabase(filename,RequestUsername)
        if not bcrypt.checkpw(RequestPassword, hashedpasswd):
            print("Wrong password")
            return("Wrong password")
        return("")
    return("No post request recived")
def writetodatabase(filename,RequestUsername):
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
                "username": RequestUsername, 
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



