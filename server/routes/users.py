from flask import request, session, jsonify, make_response
from config import db, api
from flask_restful import Resource
from models.models import User, Product, Order
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS, cross_origin

class CheckCurrentUser(Resource):
  # GET /user
  def get(self):
    user = User.query.get(session.get("user_id"))
    if user:
      return make_response(jsonify(user.to_dict()), 200)
    else:
      return {}, 204

api.add_resource(CheckCurrentUser, "/api/check-current-user")

class Signup(Resource):
  # POST /user
  @cross_origin()
  def post(self):
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    role = data.get("role")

    try:
      user = User(username=username)
      user.password_hash = password
      user.email = email
      user.role = role

      db.session.add(user)
      db.session.commit()

      session["user_id"] = user.id

      return user.to_dict(), 200
    except IntegrityError:
      return {"error": "Username already taken"}, 422
    except ValueError as error:
      return {"error": str(error)}, 422

api.add_resource(Signup, "/api/signup")

class Login(Resource):
  # POST /user
  def post(self):
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if user and user.authenticate(password):
      session["user_id"] = user.id
      return make_response(jsonify(user.to_dict()), 200)
    else:
      return {"error": "Username or Password didn't match"}, 401

api.add_resource(Login, "/api/login")

class Logout(Resource):
  # DELETE /user
  def delete(self):
    if session.get("user_id"):
      del session["user_id"]
      return {}, 204
    else:
      return {"error": "Already logged out"}, 400
  
api.add_resource(Logout, "/api/logout")

class Users(Resource):
  def get(self):
    users = [user.to_dict(only=('id', 'username', 'email', 'role',)) for user in User.query.all()]
    return make_response(jsonify(users), 200)
  
api.add_resource(Users, '/api/users')

class UserByID(Resource):
  def get(self, id):
    user = User.query.filter(User.id==id).first()

    if user:
      return make_response(user.to_dict(), 200)
  
  def patch(self, id):
    data = request.get_json()
    user = User.query.filter(User.id==id).first()

    for attr in data:
      setattr(user, attr, data.get(attr))

    db.session.add(user)
    db.session.commit()

    return make_response(user.to_dict(), 200)
  
  def delete(self, id):
    user = User.query.filter(User.id==id).first()

    if user:
      db.session.delete(user)
      db.session.commit()
      return make_response("", 204)
    else:
      return make_response(jsonify({"error": "User not found."}), 404)

api.add_resource(Users, '/api/users/<int:id>')

class Products(Resource):
  def get(self):
    products = [product.to_dict(only=('id', 'name', 'description', 'price', 'image_url', 'quantity_available', 'seller_id')) for product in Product.query.all()]
    return make_response(jsonify(products), 200)
  
class Orders(Resource):
  def get(self):
    orders = Order.query.all()

    aggregated_orders = []

    for order in orders:
      order_details = {
        'order_id': order.id,
        'status': order.status,
        'total_price': float(sum(item.product.price * item.quantity for item in order.order_items)),
        'products': [{
          'name': item.product.name,
          'quantity': item.quantity,
          'image': item.product.image_url,
          'price': item.product.price
        } for item in order.order_items]
      }
      aggregated_orders.append(order_details)
    
    return make_response(aggregated_orders, 200)

    def post(self):
      data = request.json()
      current_user_id = get_j