from . import db


class WarehouseModel(db.Model):
    __tablename__ = "warehouse"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime)
    date_tz = db.Column(db.DateTime)
    item_count = db.Column(db.Integer)
    order_id = db.Column(db.String(50))
    receive_method = db.Column(db.String(20))
    status = db.Column(db.String(20))
    store_id = db.Column(db.String(50))
    subtotal = db.Column(db.Float)
    tax_percentage = db.Column(db.Float)
    total = db.Column(db.Float)
    total_discount = db.Column(db.Float)
    total_gratuity = db.Column(db.Float)
    total_tax = db.Column(db.Float)
    updated_at = db.Column(db.DateTime)
    fulfillment_date_tz = db.Column(db.DateTime)
    user_id = db.Column(db.BigInteger)
    user_first_name = db.Column(db.String(50))
    user_last_name = db.Column(db.String(50))
    user_merchant_id = db.Column(db.String(50))
    user_phone_number = db.Column(db.BigInteger)
    user_created_at = db.Column(db.DateTime)
    user_updated_at = db.Column(db.DateTime)

    def __init__(
            self, id, created_at, date_tz, item_count,
            order_id, receive_method, status, store_id,
            subtotal, tax_percentage, total, total_discount,
            total_gratuity, total_tax, updated_at, fulfillment_date_tz,
            user_id, user_first_name, user_last_name, user_merchant_id,
            user_phone_number, user_created_at, user_updated_at
    ):
        self.id = id
        self.created_at = created_at
        self.date_tz = date_tz
        self.item_count = item_count
        self.order_id = order_id
        self.receive_method = receive_method
        self.status = status
        self.store_id = store_id
        self.subtotal = subtotal
        self.tax_percentage = tax_percentage
        self.total = total
        self.total_discount = total_discount
        self.total_gratuity = total_gratuity
        self.total_tax = total_tax
        self.updated_at = updated_at
        self.fulfillment_date_tz = fulfillment_date_tz
        self.user_id = user_id
        self.user_first_name = user_first_name
        self.user_last_name = user_last_name
        self.user_merchant_id = user_merchant_id
        self.user_phone_number = user_phone_number
        self.user_created_at = user_created_at
        self.user_updated_at = user_updated_at
