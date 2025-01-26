#!/usr/bin/python3
""" Starts a Flash Web Application """
from app.models import doctor, storage
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


@web.route('/registerDoctor', methods=['GET', 'POST'], strict_slashes=False)
def registerDoctor():
    """validate registration"""
    email = request.form.get('email')
    print(request.form.to_dict())
    # user login data validation
    if request.method == 'POST':
        # call api to save to db
        user_exists = requests.get(f'http://localhost:5000/api/v1/doctor/get_doctor_by_email/{email}')
        if user_exists.status_code == 200:
            return jsonify({'error': "That email is already in use"}), 409

        formData= request.form.to_dict()
        formData.pop('confirmPassword', None)

        response = requests.post(f'http://localhost:5000/api/v1/doctor/post_doctor/', json=formData)
        if response.status_code == 201:
            #return redirect(url_for('web.login'))
            return jsonify({'message': 'Registration successful'}), 200
        else:
            print(f"Error {response.status_code}: {response.text}")
            #return render_template('doctor_register.html', err="Registration failed. Please try again."), 400
            return jsonify({'error': "Registration failed. Please try again."}), 400
    return render_template('doctor_register.html')

@web.route('/doctors', methods=['GET', 'POST'], strict_slashes=False)
def get_all_doctors():
    """get all doctors from db"""
    print("getting")
    if request.method == 'GET':
        doctors = requests.get(f'http://localhost:5000/api/v1/doctors')

    return doctors._content

if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
