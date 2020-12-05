from flask import Flask, flash, request, redirect, url_for
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
import sqlite3
import bcrypt
conn = sqlite3.connect('database.db')
c = conn.cursor()
class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
        User(1, 'user1', 'password')
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '&RUS7vHsmj8Sa!8EWF'

jwt = JWT(app, authenticate, identity)
@app.route('/signup')
def signup():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    RequestUsername = request.authorization["username"].encode("utf-8")
    RequestPassword = request.authorization["password"].encode("utf-8")
    dbpasswd = bcrypt.hashpw(RequestPassword, bcrypt.gensalt())
    c.execute('''CREATE TABLE IF NOT EXISTS users (username,password)''')
    c.execute("INSERT INTO users VALUES (?,?);",(RequestUsername,dbpasswd))
    conn.commit()
    conn.close()
@app.route('/login')
def login():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    cursor = c.execute("SELECT username,password FROM users")
    RequestUsername = request.authorization["username"].encode("utf-8")
    RequestPassword = request.authorization["password"].encode("utf-8")
    for row in cursor:
        hashedpasswd = row[1]
    bcryptpasswd = bcrypt.hashpw(RequestPassword, bcrypt.gensalt())

    if bcrypt.checkpw(bcryptpasswd,hashedpasswd):
        print("It's alive!")
    else:
        print("Something went wrong")
    conn.close()
    return("")
 
@app.route('/protected')
@jwt_required()
def protected():
    return "Authenticated!",'%s' % current_identity

if __name__ == '__main__':
    app.run()
