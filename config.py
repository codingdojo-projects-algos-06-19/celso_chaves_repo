from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.sql import func
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import re, os, datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
app = Flask(__name__)
app.secret_key = "al;jfsaslfsadfjilkjfjifeja09u09rqrq09i"
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demo-app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

ROOT_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(ROOT_DIR, 'client', 'templates')
STATIC_DIR = os.path.join(ROOT_DIR, 'client', 'static')

app.template_folder = TEMPLATE_DIR
app.static_folder = STATIC_DIR


db = SQLAlchemy(app)
migrate = Migrate(app, db)