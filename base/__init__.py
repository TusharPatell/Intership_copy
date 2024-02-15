from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = 'EB;%n=*\B]?=&-})]o3bP?[!Sr(I?j^JaFbv(!ya+_lhvTA<CUV*QZm33b%}cy)'

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://root:root@localhost:3306/internship'

app.config['SQLALCHEMY_ECHO'] = True

app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

from base.com import controller
