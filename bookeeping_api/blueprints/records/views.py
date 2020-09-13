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
        records_list = [{"id":r.id,"date":(r.date),"description":r.description, "reference":r.reference, "amount":(r.amount / 100),"account":r.account.account_number, "account_name":r.account.name, "account_id":r.account.id } for r in Record.select().where(Record.assessment==assess.id).order_by(Record.date)]
        return jsonify({
            "status": True,
            "records": records_list,
            "assess" : assess.year_assessment
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
        """
        sample_data = {
            date: transaction-date,
            transactions: [
                {
                    account: 1, (expenses account)
                    amount: 50 , (positive => debit) convert the amount in cents before save into db (RM50 => 5000 cents)
                    description: 'any desc',
                    reference: 'document-no'
                },
                {
                    account: 2, (cash account)
                    amount: -50 , (negetive => credit)
                    description: 'any desc',
                    reference: 'document-no'
                }
            ]
        }
        data = [
            {'username': 'charlie', 'is_admin': True},
            {'username': 'huey', 'is_admin': False},
        ]
        # Insert new rows.
        query = User.insert_many(data)
        query.execute() # return number of rows modified
        """
        # loop through the transaction list, for each transaction object append into data list
        data = []
        for item in params.get('transactions'):
            data.append({
                'date': params.get('date'),
                'account': item['account'],
                'assessment': assessment.id,
                'amount': (item['amount'] * 100),
                'description': item['description'],
                'reference': item['reference']
            })
        query = Record.insert_many(data)
        if query.execute():
            return jsonify({
                "status": True,
                "message": "Successfully create records."
            })
        else:
            return jsonify({
                "status": False,
                "message": "Unable to create records."
            })
    else:
        return jsonify({
            "status": False,
            "message": "No user/assessment year found."
        })

@records_api_blueprint.route('/edit/<record_id>', methods=['POST'])
@jwt_required
def edit(record_id):
    username = get_jwt_identity()
    user = User.get_or_none(User.username==username)
    record =  Record.get_or_none(Record.id==record_id)
    if user and record.assessment.business.user==user:
        params = request.json
        record.date = params.get('date')
        record.account = params.get('account')
        record.description = params.get('description')
        record.reference = params.get('reference')
        record.amount = float(params.get('amount'))* 100
        if record.save():
            return jsonify({
                "status": True,
                "record": {
                    'date': record.date,
                    'account': record.account.id,
                    'description': record.description,
                    'reference': record.reference,
                    'amount': (record.amount / 100) ,
                },
                "message": "Successfully update record."
            })
        else:
            return jsonify({
                "status": False,
                "message": "Unable to update record."
            })
    else:
        return jsonify({
            "status": False,
            "message": "No user/record found."
        })