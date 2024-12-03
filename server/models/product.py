from config import db
from sqlalchemy_serializer import SerializerMixin

class Product(db.Model, SerializerMixin):
    _tablename__ = "products"

    serialize_rules=(
        '-orders.product', 
        '-orders.user',
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    quantity_available = db.Column(db.Integer, nullable=False)

    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    orders = db.relationship('OrderItem', backref='product', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Product {self.name} from seller {self.seller_id}>'
