from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from models.user import User
from flask_jwt_extended import create_access_token

login_api_blueprint = Blueprint('login_api',
                             __name__,
                             template_folder='templates')

@login_api_blueprint.route('/login', methods=['POST'])
def login():
  username = request.json.get("username")
  password = request.json.get("password")

  user = User.get_or_none(User.username == username)
  if user:
    result = check_password_hash(user.password_hash, password)
    if result:
      token = create_access_token(identity=user.username)
      return jsonify({
        "auth_token":token,
        "message": "Successfully logged in",
        "status":"success",
        "user": {
          "id": user.id,
          "username": user.username
        }
      }),200
    else:
      return jsonify({"error":"Wrong password. Please try again."}),401
  else:
    return jsonify({"error": "No such user. Please try again."}),401
