from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from config import db

class OrderItem(db.Model, SerializerMixin):
    __tablename__ = 'order_items'

    serialize_rules = (
        '-order',
        '-item',
    )

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    processed_date = db.Column(db.DateTime)
    item_idx = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))

    # relationship
    order = db.relationship('Order', back_populates='order_items')
    item = db.relationship('Item', back_populates='order_items')

    @validates('quantity')
    def validate(self, key, value):
        if key == 'quantity':
            if value <= 0:
                raise ValueError('Server validation error: Invalid quantity')
            
        return value

    def __repr__(self):
        return f'<OrderItem {self.id}>'