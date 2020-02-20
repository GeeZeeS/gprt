from flask.cli import FlaskGroup
from flask import send_from_directory
from project import app, db, mongo
from project.models import Warehouse

import os
import json
import re
import pandas as pd


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("populate")
def seed_mongo_db():
    # mongo.db.tr
    root_dir = app.config["STATIC_FOLDER"]
    files = os.listdir(root_dir)
    print(files)
    for _file in files:
        table_name = _file.split('_', 1)[0]
        processing_file = open(os.path.join(root_dir, _file), 'r')
        data = pd.read_csv(processing_file)
        json_data = json.loads(data.to_json(orient='records'))
        mongo.db.mng_db.remove()
        mongo.db.mng_db[table_name].insert(json_data)


if __name__ == "__main__":
    cli()
