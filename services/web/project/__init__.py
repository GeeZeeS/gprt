from flask import Flask, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
mongo = PyMongo(app)


@app.route("/")
def hello_world():
    return jsonify(hello="world")


@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)
