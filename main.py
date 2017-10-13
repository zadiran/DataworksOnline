import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import configure_app
from flask_login import LoginManager

app = Flask(__name__)
configure_app(app)

db = SQLAlchemy(app)
lm = LoginManager(app)


directory = os.path.join(app.config['BASEDIR'], 'files')
if not os.path.exists(directory):
   os.mkdir(directory)

