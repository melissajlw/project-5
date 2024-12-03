from config import db, bcrypt
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    serialize_rules=(
        '-password_hash',
        '-order.user',
        '-order.product',
    )

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    _password_hash = db.Column(db.String())
    role = db.Column(db.String(), nullable=False)

    products = db.relationship('Product', backref='seller', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True, cascade="all, delete-orphan")
    

    @hybrid_property
    def password_hash(self):
        raise Exception("Cannot access password hash")
    
    @password_hash.setter
    def password_hash(self, password):
        pw_hash = bcrypt.generate_password_hash(password)
        self._password_hash = pw_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)
    
    @validates('email')
    def validate_email(self, key, email):
        valid_endings = ["@gmail.com", "@hotmail.com", "@yahoo.com", "@aol.com", "@icloud.com", "@msn.com"]
        for ending in valid_endings:
            if email.endswith(ending):
                return email
        
        raise ValueError("Email is not valid. Please re-enter your email address.")
    
    def __repr__(self):
        return f'<User id={self.id} username={self.username}>'