import datetime
from mongoengine import Document, IntField, StringField, FloatField, DateTimeField, ReferenceField


class Users(Document):
    user_id = IntField()
    first_name = StringField()
    last_name = StringField()
    merchant_id = StringField()
    phone_number = IntField()
    created_at = DateTimeField()
    updated_at = DateTimeField()


class Orders(Document):
    id = IntField()
    created_at = DateTimeField()
    date_tz = DateTimeField()
    item_count = IntField()
    order_id = StringField()
    receive_method = StringField()
    status = StringField()
    store_id = StringField()
    subtotal = FloatField()
    tax_percentage = FloatField()
    total = FloatField()
    total_discount = IntField()
    total_gratuity = IntField()
    total_tax = FloatField()
    updated_at = FloatField()
    user_id = ReferenceField(Users)
    fulfillment_date_tz = DateTimeField()
