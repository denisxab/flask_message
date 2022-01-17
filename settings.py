import os

from flask import Flask


SETTING_DB = {"host": "localhost", "user": "root", "password": "denis0310", "database": "message_db", }
os.environ["FLASK_ENV"] = "development"
app = Flask(__name__)

# Маршрутизация
import url

url.init(app)
