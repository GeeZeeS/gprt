import redis
from flask import Flask, jsonify, send_from_directory
from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from bson.json_util import dumps
from datetime import datetime

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
mongo = app.config["MONGO_URI"].mng_db

# Connect Redis db
redis_db = redis.Redis(
    host="redis", port="6379", db=1, charset="utf-8", decode_responses=True
)

# Initialize timer in Redis
redis_db.mset({"minute": 0, "second": 0})

# Add periodic tasks
celery_beat_schedule = {
    "time_scheduler": {
        "task": "app.timer",
        # Run every second
        "schedule": 1.0,
    }
}

celery = Celery(app.name)
celery.conf.update(
    result_backend=app.config["CELERY_RESULT_BACKEND"],
    broker_url=app.config["CELERY_BROKER_URL"],
    timezone="UTC",
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    beat_schedule=celery_beat_schedule,
)


@app.route("/<db_name>")
def mongo_preview(db_name):
    data = mongo.db.mng_db[db_name].find({}).limit(10)
    return dumps(data)


@app.route("/joined")
def joined_tables():
    filter_date_end = datetime(2020, 1, 1)
    filter_date_start = datetime(2019, 1, 1)
    data_set = mongo.db.mng_db['orders'].find(
        {
            "created_at": {
                "$gte": str(filter_date_start),
                "$lt": str(filter_date_end)
            }
        }
    ).sort([("created_at", -1)]).limit(500)

    final = []
    for data in data_set:
        users = mongo.db.mng_db['users'].find({"user_id": data['user_id']})
        for user in users:
            data['user'] = user
            final.append(data)
    return dumps(final)


@app.route("/one_row")
def one_row_tables():
    data_set = mongo.db.mng_db['orders'].find({}).limit(10)
    final = []
    for data in data_set:
        users = mongo.db.mng_db['users'].find({"user_id": data['user_id']})
        for user in users:
            del data['user_id']
            new_user = {key: user[key] for key in user if key != 'user' and key != '_id'}
            data.update(user)
            final.append(data)
    return dumps(final)
