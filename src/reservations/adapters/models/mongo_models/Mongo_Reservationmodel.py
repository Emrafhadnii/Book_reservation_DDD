from mongoengine import IntField,DateTimeField,Document

class Reservation(Document):
    id = IntField(primary_key=True)
    customer_id = IntField('Customer', required=True)
    book_id = IntField('Book', required=True)
    start_time = DateTimeField(required=True)
    end_time = DateTimeField(required=True)
    price = IntField(default=0)

    meta = {
        'collection': 'reservations'
    }