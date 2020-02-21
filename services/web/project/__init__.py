from flask import Flask, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from bson.json_util import dumps

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
mongo = app.config["MONGO_URI"].mng_db


@app.route("/<db_name>")
def mongo_preview(db_name):
    data = mongo.db.mng_db[db_name].find({}).limit(10)
    return dumps(data)


@app.route("/joined")
def joined_tables():
    data_set = mongo.db.mng_db['orders'].find({}).limit(10)
    final = []
    for data in data_set:
        users = mongo.db.mng_db['users'].find({"user_id": data['user_id']})
        for user in users:
            data['user'] = user
            del data['user_id']
            final.append(data)
    return dumps(final)
