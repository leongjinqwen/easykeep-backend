from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.account import Account
from models.business import Business

accounts_api_blueprint = Blueprint('accounts_api',
                             __name__,
                             template_folder='templates')

@accounts_api_blueprint.route('/<business_id>', methods=['GET'])
@jwt_required
def index(business_id):
    username = get_jwt_identity()
    user = User.get_or_none(User.username==username)
    business = Business.get_or_none(Business.id==business_id, Business.user==user)
    if user and business:
        account_list = [{"id":a.id,"name":a.name,"number":a.account_number,"type":a.acc_type } for a in Account.select().where(Account.business==business.id).order_by(Account.acc_type) ]
        return jsonify({
            "status": True,
            "accounts": account_list
        })
    else:
        return jsonify({
            "status": False,
            "message": "No user/business found."
        })

        
@accounts_api_blueprint.route('/<business_id>', methods=['POST'])
@jwt_required
def create(business_id):
    username = get_jwt_identity()
    user = User.get_or_none(User.username==username)
    business = Business.get_or_none(Business.id==business_id, Business.user==user)
    if user and business:
        account = Account(name=request.json.get('name'), business=business, account_number=request.json.get('acc_num'),acc_type=request.json.get('acc_type'))
        if account.save():
            return jsonify({
                "status": True,
                "account": {
                    'id':account.id,
                    'name':account.name,
                    'acc_num':account.account_number,
                    'acc_type':account.acc_type
                },
                "message": "Successfully create new account."
            })
        else:
            return jsonify({
                "status": False,
                "message": "Unable to create new account."
            })
    else:
        return jsonify({
            "status": False,
            "message": "No user/business found."
        })


