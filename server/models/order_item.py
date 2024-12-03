from config import db
from sqlalchemy_serializer import SerializerMixin

class OrderItem(db.Model, SerializerMixin):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    #serialize_rules = ('-order.order_items', '-product.orders',)

    def __repr__(self):
        return f'<OrderItem {self.id}>'