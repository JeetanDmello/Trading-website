from flask import Flask, render_template, request, url_for, session
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin
import mysql.connector
import re

app = Flask(__name__)

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = ""
)

cursor = db.cursor()
cursor.execute("use db")
db.commit()


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")


@app.route('/login', methods=['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor.execute('SELECT * FROM users WHERE username = % s AND user_password = % s', (username, password, ))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'    
            return render_template('index.html', msg = msg)

        else:
            msg = 'Incorrect username / password !'

    return render_template('login.html', msg = msg)

@app.route('/sign-up', methods=['GET','POST'])
def sign_up():
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'check_password' in request.form:
        username = request.form['username']
        password = request.form['password']
        check_password = request.form['check_password']
        email = request.form['email']
        cursor.execute('SELECT * FROM user WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        elif check_password != password:
            msg = 'passwords are not the same !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            db.commit()
            msg = 'You have successfully registered !'
            return render_template('login.html', msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'

    return render_template('sign_up.html', msg = msg)


if __name__ == "__main__":
    app.run(debug=True)