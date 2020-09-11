from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.business import Business
from models.assessment import Assessment

assessment_api_blueprint = Blueprint('assessment_api',
                             __name__,
                             template_folder='templates')

@assessment_api_blueprint.route('/<business_id>', methods=['GET'])
@jwt_required
def index(business_id):
    username = get_jwt_identity()
    user = User.get_or_none(User.username==username)
    business = Business.get_or_none(Business.id==business_id, Business.user==user)
    if user and business:
        assessments = [{"id":a.id,"y_a":a.year_assessment,"y_e":a.year_ended} for a in Assessment.select().where(Assessment.business==business.id)]
        return jsonify({
            "status": True,
            "assessments": assessments
        }),200
    else:
        return jsonify({
            "status": False,
            "message": "No user/business found."
        }),401

        
@assessment_api_blueprint.route('/<business_id>', methods=['POST'])
@jwt_required
def create(business_id):
    username = get_jwt_identity()
    user = User.get_or_none(User.username==username)
    business = Business.get_or_none(Business.id==business_id, Business.user==user)
    if user and business:
        assess = Assessment(year_assessment=request.json.get('y_a'), year_ended=request.json.get('y_e'), business=business)
        if assess.save():
            return jsonify({
                "status": True,
                "message": "Successfully create new assessment year.",
                "assessment": {
                    "id": assess.id,
                    "business": business.name,
                    "y_a": assess.year_assessment,
                    "y_e": assess.year_ended
                }
            }),200
        else:
            return jsonify({
                "status": False,
                "message": "Unable to create new assessment year."
            }),404
    else:
        return jsonify({
            "status": False,
            "message": "No user/business found."
        }),401


@assessment_api_blueprint.route('/show/<assess_id>', methods=['GET'])
@jwt_required
def show(assess_id):
    username = get_jwt_identity()
    user = User.get_or_none(User.username==username)
    assess = Assessment.get_or_none(Assessment.id==assess_id)
    if user and assess:
        accounts = [{"id":acc.id,"name":acc.name,"acc_num":acc.account_number, "acc_type":acc.acc_type} for acc in assess.business.accounts]
        assessment = { "id":assess.id,"y_a":assess.year_assessment,"y_e":assess.year_ended, "business_id":assess.business.id,"business": assess.business.name, }
        return jsonify({
            "status": True,
            "assessment": assessment,
            
            "accounts" : accounts
        }),200
    else:
        return jsonify({
            "status": False,
            "message": "No user/assessment found."
        }),401