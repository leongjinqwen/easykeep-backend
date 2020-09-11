from app import app,csrf
from flask_cors import CORS

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
## API Routes ##
from bookeeping_api.blueprints.users.views import users_api_blueprint
from bookeeping_api.blueprints.login.views import login_api_blueprint
from bookeeping_api.blueprints.records.views import records_api_blueprint
from bookeeping_api.blueprints.business.views import business_api_blueprint
from bookeeping_api.blueprints.assessment.views import assessment_api_blueprint
from bookeeping_api.blueprints.accounts.views import accounts_api_blueprint


app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')
app.register_blueprint(login_api_blueprint, url_prefix='/api/v1/')
app.register_blueprint(records_api_blueprint, url_prefix='/api/v1/records')
app.register_blueprint(business_api_blueprint, url_prefix='/api/v1/business')
app.register_blueprint(assessment_api_blueprint, url_prefix='/api/v1/assessment')
app.register_blueprint(accounts_api_blueprint, url_prefix='/api/v1/accounts')

csrf.exempt(users_api_blueprint)
csrf.exempt(login_api_blueprint)
csrf.exempt(records_api_blueprint)
csrf.exempt(business_api_blueprint)
csrf.exempt(assessment_api_blueprint)
csrf.exempt(accounts_api_blueprint)
