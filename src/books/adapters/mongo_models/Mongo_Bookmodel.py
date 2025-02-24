from mongoengine import Document,StringField,IntField,ReferenceField

class Book(Document):
    id = IntField(primary_key=True)
    title = StringField(max_length=200, required=True)
    isbn = StringField(max_length=13, unique=True, required=True)
    price = IntField(required=True)
    book_desc = StringField(max_length=100, default='')
    units = IntField(required=True)
    genre_id = IntField(required=True)
    
    meta = {
        'collection': 'books'
    }