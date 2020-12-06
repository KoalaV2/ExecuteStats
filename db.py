#!/usr/bin/env python3
import sqlite3
import bcrypt
conn = sqlite3.connect('/home/koala/programming/python/ExecuteStats/database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (username,password)''')
username = input("What is the name of the user? \n :").encode("utf-8")
passwd = input("What is the password of the user going to be? \n : ").encode("utf-8")
hashed = bcrypt.hashpw(passwd, bcrypt.gensalt())
c.execute("INSERT INTO users VALUES (?,?);",(username,hashed))
conn.commit()
conn.close()
