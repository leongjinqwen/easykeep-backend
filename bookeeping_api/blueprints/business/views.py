from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.business import Business

business_api_blueprint = Blueprint('business_api',
                             __name__,
                             template_folder='templates')

@business_api_blueprint.route('/', methods=['GET'])
@jwt_required
def index():
    username = get_jwt_identity()
    user = User.get_or_none(User.username==username)
    if user:
        business_list = [{"id":b.id,"name":b.name} for b in Business.select().where(Business.user==user)]
        return jsonify({
            "status": True,
            "businesses": business_list
        })
    else:
        return jsonify({
            "status": False,
            "message": "No user found."
        })

        
@business_api_blueprint.route('/', methods=['POST'])
@jwt_required
def create():
    username = get_jwt_identity()
    user = User.get_or_none(User.username==username)
    if user:
        business = Business(name=request.json.get('name'), user=user)
        if business.save():
            return jsonify({
                "status": True,
                "message": "Successfully create new business.",
                "business": {
                    "id": business.id,
                    "name": business.name
                }
            }),200
        else:
            return jsonify({
                "status": False,
                "message": "Unable to create new business."
            }),400
    else:
        return jsonify({
            "status": False,
            "message": "No user found."
        }),401


