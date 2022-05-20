from flask import Flask
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
db = SQLAlchemy(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:HoangKiet12@localhost/hotel"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hotel.db"
app.config["SECRET_KEY"] = "fa3453722a1cefec27f0472e"

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'HoangKiet12'
app.config['MYSQL_DB'] = 'hotel'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from hotel import routes
