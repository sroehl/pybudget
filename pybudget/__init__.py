from flask import Flask

app = Flask(__name__,  static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
ALLOWED_EXTENSIONS = {'csv'}

app.secret_key = 'SUPERSECRET'

from pybudget import routes
