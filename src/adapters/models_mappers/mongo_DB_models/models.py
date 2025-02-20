from mongoengine import Document, StringField, IntField, ListField, EmbeddedDocumentField, EmbeddedDocument, DateTimeField
from src.domain.enums import UserRole, SubscriptionModel

class Book(Document):
    title = StringField(required=True, max_length=200)
    isbn = StringField(required=True, unique=True, max_length=13)
    price = IntField(required=True)
    genre_id = IntField()
    book_desc = StringField(default="")
    units = IntField(required=True)
    meta = ""