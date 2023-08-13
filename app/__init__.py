from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from flask_mail import Mail
from flask_rq2 import RQ
from flask_caching import Cache
from celery import Celery
import pytz

app = Flask(__name__, template_folder='../templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tshow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'sahilbhure1021'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'madhurimuke24@gmail.com'
app.config['MAIL_PASSWORD'] = 'icobcjyunbteepta'

cache = Cache(config={'CACHE_TYPE': 'redis',
                      'CACHE_REDIS_HOST': 'localhost',  
                      'CACHE_REDIS_PORT': 6379,         
                      'CACHE_REDIS_URL': 'redis://localhost:6379/0'})
cache.init_app(app)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0' 
app.config['result_backend'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], result_backend=app.config['result_backend'],include=['app.tasks'])
celery.conf.update(app.config)

db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app, origins=['http://localhost:8080'], supports_credentials=True, expose_headers=['Authorization'])

migrate = Migrate(app, db)
mail = Mail(app)
rq = RQ(app)
cache = Cache(config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_HOST': 'localhost', 'CACHE_REDIS_PORT': 6379, 'CACHE_REDIS_URL': 'redis://localhost:6379/0'})
cache.init_app(app)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], result_backend=app.config['result_backend'])
celery.conf.update(app.config)
# app.conf.timezone = 'Asia/Kolkata'

from app import models, controllers, tasks, workers
