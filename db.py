#!/usr/bin/env python3

import bcrypt
import sqlite3
conn = sqlite3.connect('database.db')
c = conn.cursor()
def writepasswd():
    c.execute('''CREATE TABLE IF NOT EXISTS users (username,password)''')
    username = input("What is your username? \n :") 
    passwd = input("What is your password? \n :").encode("utf-8")
    hashed = bcrypt.hashpw(passwd, bcrypt.gensalt())
    c.execute("INSERT INTO users VALUES (?,?);",(username,hashed))
    conn.commit()
    conn.close()
    return passwd,hashed
def checkpasswd():
    dbpasswdInput = input("Please enter your password \n : ").encode("utf-8")
    dbpasswd = bcrypt.hashpw(dbpasswdInput, bcrypt.gensalt())
    cursor= c.execute("SELECT username,password FROM users")
    for row in cursor:
        print("USERNAME = ", row[0])
        print("HASHEDPASSWD = ", row[1])
        hasheddb = row[1]
        print("DBPASSWD = ", dbpasswd)
    if bcrypt.checkpw(dbpasswd,hasheddb):
        print("It matches!")
    else:
        print("Doesnt match")
    conn.close()
def main():
    choice = input("signup, delete or login? \n :")
    if choice == "signup":
        writepasswd()
    elif choice == "login":
        checkpasswd()
    else:
        print("Something went wrong")
if __name__ == "__main__":
    main()
