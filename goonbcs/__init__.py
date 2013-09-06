# Copyright (c) 2013 Peter Rowlands

"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

from __future__ import absolute_import

import os

from flask import Flask
from flask.ext.heroku import Heroku
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.sqlalchemy import SQLAlchemy

from .models import User, Role

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY',
                                          'this_should_be_configured')

# flask-heroku
heroku = Heroku(app)

# flask-sqlalchemy
db = SQLAlchemy(app)

# flask-security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

from . import views
