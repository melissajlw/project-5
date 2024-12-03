from flask import request, session, jsonify, make_response
from config import db, api
from flask_restful import Resource
from models.models import User
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS, cross_origin

class CheckCurrentUser(Resource):
  # GET /user
  def get(self):
    user = User.query.get(session.get("user_id"))
    if user:
      return user.to_dict(), 200
    else:
      return {}, 204

api.add_resource(CheckCurrentUser, "/api/check-current-user")

class SignupResource(Resource):
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

api.add_resource(SignupResource, "/api/signup")

class LoginResource(Resource):
  # POST /user
  def post(self):
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
      return jsonify({'error': 'Unauthorized'}), 401
    
    if not user.authenticate(password):
      return {"error": "Username or Password didn't match"}, 422

    session["user_id"] = user.id
    return user.to_dict(), 200


api.add_resource(LoginResource, "/api/login")

class LogoutResource(Resource):
  # DELETE /user
  def delete(self):
    if session.get("user_id"):
      del session["user_id"]
      return {}, 204
    else:
      return {"error": "Already logged out"}, 400
  
api.add_resource(LogoutResource, "/api/logout")

class UsersResource(Resource):
  def get(self):
    users = [user.to_dict() for user in User.query.all()]
    return users, 200
  
api.add_resource(UsersResource, '/api/users')

class UserResource(Resource):
  def get(self, id):
    user = User.query.get(id)
    return user.to_dict(), 200
  
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

api.add_resource(UserResource, '/api/users/<int:id>')