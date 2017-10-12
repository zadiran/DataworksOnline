import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager

app = Flask(__name__)
#app.debug = True
app.config.from_object(Config())
app.config['BASEDIR'] = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
lm = LoginManager(app)


directory = os.path.join(app.config['BASEDIR'], 'files')
if not os.path.exists(directory):
   os.mkdir(directory)

