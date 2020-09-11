from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.record import Record
from models.account import Account
from models.assessment import Assessment

records_api_blueprint = Blueprint('records_api',
                             __name__,
                             template_folder='templates')

@records_api_blueprint.route('/<assessment_id>', methods=['GET'])
@jwt_required
def index(assessment_id):
    username = get_jwt_identity()
    user = User.get_or_none(User.username==username)
    assess = Assessment.get_or_none(Assessment.id==assessment_id)
    if user and assess.business.user==user:
        records_list = [{"id":r.id,"date":r.date,"description":r.description,"amount":float(r.amount),"acc_num":r.account.account_number } for r in Record.select().where(Record.assessment==assess.id)]
        return jsonify({
            "status": True,
            "records": records_list
        })
    else:
        return jsonify({
            "status": False,
            "message": "No user/assessment found."
        })

@records_api_blueprint.route('/<assessment_id>', methods=['POST'])
@jwt_required
def create(assessment_id):
    username = get_jwt_identity()
    user = User.get_or_none(User.username==username)
    assessment = Assessment.get_or_none(Assessment.id==assessment_id)
    if user and assessment.business.user==user:
        params = request.json
        record = Record(amount=params.get('amount'),date=params.get('date'),account=params.get('account'),assessment=assessment,description=params.get('description'))
        if record.save():
            return jsonify({
                "status": True,
                "message": "Successfully create new record."
            })
        else:
            return jsonify({
                "status": False,
                "message": "Unable to create new record."
            })
    else:
        return jsonify({
            "status": False,
            "message": "No user/assessment year found."
        })
