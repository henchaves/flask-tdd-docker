from flask import Blueprint, request
from flask.wrappers import Response
from flask_restx import Resource, Api

from src import db
from src.api.models import User

users_blueprint = Blueprint("users", __name__)
api = Api(users_blueprint)

class UsersList(Resource):
  
  def post(self):
    post_data = request.get_json()
    username = post_data.get("username")
    email = post_data.get("email")
    response_object = {}

    user = User.query.filter_by(email=email).first()
    if user:
      response_object["message"] = "Sorry. That email already exists."
      return response_object, 400

    db.session.add(User(username=username, email=email))
    
    try:
      db.session.commit()

      response_object["message"] = f"{email} was added!"
      return response_object, 201
    
    except:
      db.session.rollback()

api.add_resource(UsersList, "/users")