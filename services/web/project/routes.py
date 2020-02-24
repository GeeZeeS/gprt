from . import app, mongo
from bson.json_util import dumps


@app.route("/<db_name>")
def mongo_preview(db_name):
    data = mongo.db.mng_db[db_name].find({}).limit(10)
    return dumps(data)