#!/usr/bin/python3
""" Starts a Flash Web Application """
from app.models import patient, storage
from app.api.v1.web import web
from os import environ
from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
from hashlib import md5
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


@web.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """render the login form"""
    formData = request.form.to_dict()

    # user login data validation
    if request.method == 'GET':
        # redirect if session exists
        if session:
            if session.get('role') == 'patient':
                return redirect(url_for('web.patientD'))
            elif session.get('role') == 'doctor':
              return redirect(url_for('web.doctorD'))
            else:
              pass
        # default if no session
        return render_template('login.html')

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        # query from db the specific user based on email

        if role == "doctor":
            try:
                response = requests.get(f'http://localhost:5000/api/v1/doctor/get_doctor_by_email/{email}')
            except Exception as e:
                return render_template('login', err="email or password is incorrect")
        elif role == "patient":
            try:
                response = requests.get(f'http://localhost:5000/api/v1/patient/get_patient_by_email/{email}')
            except Exception as e:
                return render_template('login', err="email or password is incorrect")

        user_data = response.json()
        
        if response.status_code == 200:
            user = user_data
            pwd = md5(password.encode()).hexdigest()
            userPC = user.get('pCode')
            userRole = user.get('role')

            if user and (userPC == pwd):
                session['email'] = email
                session['role'] = userRole

                if session['email']:
                    print("session stored")
                if session["role"] == 'doctor':
                    return redirect(url_for('web.doctorD'))
                elif session["role"] == 'patient':
                    return redirect(url_for('web.patientD'))
            else:
                error = "email or password is incorrect"
                return render_template('login.html', err=error)

        return render_template('login.html', err="email or password is incorrect")



if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
