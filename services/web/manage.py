from flask.cli import FlaskGroup

from project import app, db
from project.models import Warehouse


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


# @cli.command("populate")
# def seed_db():
#     db.session.commit()


if __name__ == "__main__":
    cli()
