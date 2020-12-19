#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""Module init file"""

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'skey';

lman = LoginManager()
lman.init_app(app)

from app import routes

