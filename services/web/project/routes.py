from . import app, mongo
from flask import jsonify, make_response
from bson.json_util import dumps
from .models import WarehouseModel
from sqlalchemy import desc


@app.route("/")
def mongo_preview():
    return jsonify(
        {
            "query": list(
                map(
                    lambda dev: dev.serialize(),
                    WarehouseModel.query.order_by(desc('created_at')).limit(10)
                              )
                          )
        }
    )
