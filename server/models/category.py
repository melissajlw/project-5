from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from config import db

class Category(db.Model, SerializerMixin):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    items = db.relationship('Item', back_populates='category', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Category {self.id}>'