from flask import Flask
from flask_login import LoginManager
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
ALLOWED_EXTENSIONS = {'csv'}

login = LoginManager(app)
login.login_view = 'login'

# For RESTAPI auth
auth = HTTPBasicAuth()

app.secret_key = 'SUPERSECRET'

from pybudget import routes
