from config import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    serialize_rules = (
        '-item.category',
        '-item.seller',
        '-item.cart_items',
        '-item.order_items',
        '-item.reviews',
        '-customer.user', 
        '-customer.cart_items', 
        '-customer.cart_items', 
        '-customer.reviews', 
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    rating = db.Column(db.Integer, nullable=False)
    headline = db.Column(db.String)
    content = db.Column(db.String)
    images = db.Column(db.String)
    review_done = db.Column(db.Integer)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))

    item = db.relationship('Item', back_populates='reviews')
    customer = db.relationship('Customer', back_populates='reviews')

    @validates('rating', 'review_done')
    def validate(self, key, value):
        if key == 'rating':
            if value < 1 or value > 5:
                raise ValueError('Server validation error: Invalid rating')
        elif key == 'review_done':
            if value not in [0, 1]:
                raise ValueError('Server validation error: Invalid review_done')

        return value

    def __repr__(self):
        return f'<Review {self.id}>'