#!/usr/bin/python3
""" Flask Application """
from app.api.v1.utils import app_views
import binascii
from app.api.v1.web import web
from dotenv import load_dotenv
from datetime import timedelta
from app.models import storage
import os
from os import environ
from os import getenv
from flask import Flask, render_template, make_response, jsonify, request, session
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from
from flask_debugtoolbar import DebugToolbarExtension

load_dotenv()

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(web)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.secret_key = binascii.hexlify(os.urandom(24)).decode()

toolbar = DebugToolbarExtension(app)

@app.teardown_appcontext
def close_db(error):
    """closes data base connection on flask app close"""
    if storage:
        storage.close()
    else:
        print("Storage is None, cannot close")

@app.before_request
def log_request_path():
    print(f"Accessing route: {request.path}")

@app.before_request
def make_session_permanent():
    session.permanent = True  # Make the session permanent
    app.permanent_session_lifetime = timedelta(days=7)  # Session las

@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    print("Routes available:", app.url_map)

    return render_template('error.html')

app.config['SWAGGER'] = {
    'title': 'my appointment Restful API',
    'uiversion': 3
}

Swagger(app)


if __name__ == "__main__":
    """ Main Function """
    host = environ.get('MYAPPOINTMENT_API_HOST')
    port = environ.get('MYAPPOINTMENT_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, debug=True, threaded=True)
