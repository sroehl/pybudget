import plaid
from flask import Flask
from flask_login import LoginManager
from flask_httpauth import HTTPBasicAuth
from dotenv import load_dotenv
from os import getenv

# Load settings from .env file
load_dotenv()

app = Flask(__name__, static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
ALLOWED_EXTENSIONS = {'csv'}

client = plaid.Client(client_id=getenv("PLAID_CLIENT_ID"),
                      secret=getenv("PLAID_SECRET"),
                      environment=getenv("PLAID_ENV"),
                      api_version='2019-05-29')

login = LoginManager(app)
login.login_view = 'login'

# For RESTAPI auth
auth = HTTPBasicAuth()

app.secret_key = 'SUPERSECRET'

from pybudget import routes
