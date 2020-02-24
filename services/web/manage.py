from flask.cli import FlaskGroup
from project import app, db, mongo

import os
import io
import json
import pandas as pd


cli = FlaskGroup(app)
mng = mongo.db.mng_db


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("populate")
def seed_mongo_db():
    root_dir = app.config["STATIC_FOLDER"]
    # Getting files inside static folder
    files = os.listdir(root_dir)
    # Processing files
    for _file in files:
        # Getting table name based on file name
        table_name = _file.split('_', 1)[0]
        print(f'Fetching data from {_file}, into table {table_name}')
        # Opening File and working with it
        with io.open(os.path.join(root_dir, _file), 'r', encoding="utf-8") as processing_file:
            data = pd.read_csv(processing_file)
            json_data = json.loads(data.to_json(orient='records'))
            # Drop tables that where already populated
            print(f'Clearing table "{table_name}"')
            mng[table_name].drop()
            # Writing Data to DB
            print(f'Writing Data to table "{table_name}"')
            mng[table_name].insert_many(json_data)
            print(f'Table {table_name} created and data was inserted, \n'
                  f'total {mng[table_name].estimated_document_count()} rows')


if __name__ == "__main__":
    cli()
