from . import db


class Warehouse(db.Model):
    __tablename__ = "warehouse"

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    merchant = db.Column(db.String(50))
    phone_number = db.Column(db.String(50))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
