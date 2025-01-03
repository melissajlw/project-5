from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from config import db, bcrypt

class Seller(db.Model, SerializerMixin):
    __tablename__ = 'sellers'

    serialize_rules = (
        '-user',
        '-items',
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', back_populates='seller')
    items = db.relationship('Item', back_populates='seller', cascade='all, delete-orphan')

    @validates('name')
    def validate(self, key, value):
        if key == 'name':
            if len(value) == 0:
                raise ValueError('Server validation error: No name')
        
        return value

    def __repr__(self):
        return f'<Seller {self.id}>'
