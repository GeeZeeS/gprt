import os
from pymongo import MongoClient

basedir = os.path.abspath(os.path.dirname(__file__))

DBUSER = 'user'
DBPASS = '2wsx#EDC'
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'pg_db'


class Config(object):
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DBUSER}:{DBPASS}@{DBHOST}:{DBPORT}/{DBNAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = f"{os.getenv('APP_FOLDER')}/project/static"
    MONGO_URI = MongoClient("mongodb://mongo:27017")
    CELERY_BROKER_URL = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND = "redis://redis:6379/0"
