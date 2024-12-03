from config import db
from sqlalchemy_serializer import SerializerMixin

class Order(db.Model, SerializerMixin):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False)  # e.g., 'pending', 'shipped', 'delivered'

    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")

    #serialize_rules = ('-user.orders', '-product.orders',)

    def __repr__(self):
        return f'<Order {self.id}>'