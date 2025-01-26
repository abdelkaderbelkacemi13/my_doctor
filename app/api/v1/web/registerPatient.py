#!/usr/bin/python3
""" Starts a Flash Web Application """
from app.models import patient, storage
from app.api.v1.web import web
from os import environ
from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify, abort
import requests
import uuid
from werkzeug.security import check_password_hash
import json

app = Flask(__name__)
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@web.route('/registerPatient', methods=['GET', 'POST'], strict_slashes=False)
def registerPatient():
    """validate registration"""
    formData = request.form.to_dict()
    email = request.form.get('email')
    # user login data validation
    if request.method == 'POST':
        # call api to save to db
        user_exists = requests.get(f'http://localhost:5000/api/v1/patient/get_patient_by_email/{email}')
        #if user_exists:
        #    return render_template('patient_register.html', err="That email is already in use")
        if user_exists.status_code == 200:
            return jsonify({'error': "That email is already in use"}), 409
        
        formData.pop('confirmPassword')
        response = requests.post(f'http://localhost:5000/api/v1/patient/post_patient/', json=formData)
        if response.status_code == 201:
            return jsonify({'message': 'Registration successful'}), 200
        else:
            print(f"Error {response.status_code}: {response.text}")
            return jsonify({'error': "Registration failed. Please try again."}), 400
    return render_template('patient_register.html')


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
