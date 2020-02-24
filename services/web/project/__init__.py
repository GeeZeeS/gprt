from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from redis import Redis


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
mongo = app.config["MONGO_URI"].mng_db

redis = Redis(host='redis', port=6379)
scheduler = BackgroundScheduler()

from .routes import mongo_preview, joined_tables, one_row_tables
from .jobs import main_job
