# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

DB_USER = 'root'
DB_PSWD = 'root'
DB_FORMAT = 'mysql://%s:%s@localhost:3306/cyanit'

app.config['SQLALCHEMY_DATABASE_URI'] = DB_FORMAT % (DB_USER, DB_PSWD)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Flask please keep this secret for me'

db = SQLAlchemy(app)
db.init_app(app)

from cyanit import views
from cyanit import models
