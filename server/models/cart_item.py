from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from config import db

class CartItem(db.Model, SerializerMixin):
    __tablename__ = 'cart_items'

    serialize_rules = (
        '-item.category',
        '-item.seller',
        '-item.cart_items',
        '-customer',
    )

    id = db.Column(db.Integer, primary_key=True)
    checked = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    item_idx = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))

    item = db.relationship('Item', back_populates='cart_items')
    customer = db.relationship('Customer', back_populates='cart_items')

    @validates('quantity')
    def validate(self, key, value):
        if key == 'quantity':
            if value <= 0:
                raise ValueError('Server validation error: Invalid quantity')
        
        return value

    def __repr__(self):
        return f'<CartItem {self.id}>'