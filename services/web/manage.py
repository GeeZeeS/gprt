from flask.cli import FlaskGroup

from project import app, db, mongo
from project.models import Warehouse


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("populate")
def seed_mongo_db():
    db = mongo.db.data


if __name__ == "__main__":
    cli()
