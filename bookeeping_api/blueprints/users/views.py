from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.business import Business
from flask_jwt_extended import create_access_token

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    users = []
    for u in User.select():
        users.append({
            "id" : u.id,
            "username" : u.username,
            "email" : u.email
        })
    return jsonify({
        "users" : users 
    })

@users_api_blueprint.route('/', methods=['POST'])
def create():
    params = request.json
    user = User(username=params.get("username"),password=params.get("password"),email=params.get("email"))
    if user.save():
        token = create_access_token(identity=user.username)
        return jsonify({
            "auth_token":token,
            "message" : "Successfully sign up and sign in.",
            "user" : {
                "id" : user.id,
                "username" : user.username
            } 
        }),200
    else :
        return jsonify({
            "message" : "Unable to sign up. Try again.",
            "errors" : user.errors                                          
        }), 400


@users_api_blueprint.route('/<user_id>', methods=['GET'])
@jwt_required
def show(user_id):
  username = get_jwt_identity()
  user = User.get_or_none(User.username==username)

  if user:
    business_list = [{"id":b.id,"name":b.name} for b in Business.select().where(Business.user==user)]
    return jsonify({
      'user' : {
        "id": user.id,
        "username": user.username,
        "email": user.email,
      },
      "businesses": business_list,
      'status': True
    }),200
  else :
    return jsonify({
      "status": False,
      'message':'No such user.'
    }), 404



