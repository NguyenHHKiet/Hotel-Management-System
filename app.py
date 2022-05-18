from flask import Flask, render_template, make_response, flash, redirect, url_for, session, request, logging
import random
from flask_mysqldb import MySQL
from flask_wtf import Form
from wtforms import DateField, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import pdfkit
from twilio.rest import Client
from datetime import date
import os


app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'HoangKiet12'
app.config['MYSQL_DB'] = 'hotel_mgmt'

# init MYSQL
mysql = MySQL(app)



# routes
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')
    
    









    
if __name__ == '__main__':
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY

    print(SECRET_KEY)

    SECRET_KEY = os.urandom(32)
    app.config['WTF_CSRF_SECRET_KEY']=SECRET_KEY

    app.run(debug = True)