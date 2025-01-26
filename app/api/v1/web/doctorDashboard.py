#!/usr/bin/python3
""" Starts a Flash Web Application """
from app.models import storage
from app.api.v1.web import web
from os import environ
import requests
from flask import Flask, render_template, redirect, url_for, session, jsonify
import uuid
app = Flask(__name__)
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()

@web.route('/doctor/dashboard', strict_slashes=False)
def doctorD():
    """render the register form"""
    if session.get('role') != 'doctor':
        return redirect(url_for('web.login'))
    email = session.get('email')
    print("initializinf req...")
    appointementReq = requests.get(f'http://localhost:5000/api/v1/appointment/get_appointment_by_doctor_email/{email}')
    print('req finalized...')
    # print(appointementReq.json())

    appointmentRequests = []
    bookedAppointments=[]
    if appointementReq.status_code == 404:
        appointmentRequests = None
    else:
        for appointment in appointementReq.json():
            patient_email = appointment.get('patient_email')
            patient = requests.get(f'http://localhost:5000/api/v1/patient/get_patient_by_email/{patient_email}').json()
            patient_tel = patient.get('tel')
            first_name = patient.get('first_name')
            last_name = patient.get('last_name')
            print(first_name, last_name)
            approved = appointment.get('approved')
            
            if approved == 'approved':
                bookedAppointments.append({
                    'first_name' : first_name,
                    'last_name': last_name,
                    'patient_email': patient_email,
                    'patient_number': patient_tel,
                    'date': appointment.get('date'),
                    'id': appointment.get('id'),
                    'approved': appointment.get('approved')})
            elif approved == 'pending':
                appointmentRequests.append({
                    'first_name' : first_name,
                    'last_name': last_name,
                    'patient_email': patient_email,
                    'patient_number': patient_tel,
                    'date': appointment.get('date'),
                    'id': appointment.get('id'),
                    'approved': appointment.get('approved')})
            else:
                pass


    return render_template('doctor_dashboard.html', appointmentRequests=appointmentRequests, bookedAppointments=bookedAppointments )


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
