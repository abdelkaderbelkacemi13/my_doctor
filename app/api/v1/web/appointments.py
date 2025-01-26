#!/usr/bin/python3
""" Starts a Flash Web Application """
from app.models import storage
from app.api.v1.web import web
from os import environ
import requests
from flask import Flask, render_template, redirect, url_for, session, request, jsonify
import uuid
app = Flask(__name__)
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@web.route('/patient/appointments', strict_slashes=False)
def administratorD():
    """render the appointment page"""
    if session.get('role') != 'patient':
        return redirect(url_for('web.login'))
    # get appointments by user email
    email = session.get('email')
    print("initializinf req...")
    appointementReq = requests.get(f'http://localhost:5000/api/v1/appointment/get_appointment_by_patient_email/{email}')
    print('req finalized...')

    appointments=[]
    if appointementReq.status_code == 404:
        appointmentRequests = None
    else:
        for appointment in appointementReq.json():
            doctor_email = appointment.get('doctor_email')
            print(doctor_email)
            doctor = requests.get(f'http://localhost:5000/api/v1/doctor/get_doctor_by_email/{doctor_email}').json()
            specalization = doctor.get('specialization')
            first_name = doctor.get('first_name')
            last_name = doctor.get('last_name')
            print(first_name, last_name)
            approved = appointment.get('approved')

            appointments.append({
                'first_name' : first_name,
                'last_name': last_name,
                'doctor_email': doctor_email,
                'specalization': specalization,
                'date': appointment.get('date'),
                'id': appointment.get('id'),
                'approved': approved})
            
    return render_template('appointments.html', appointments=appointments)

@web.route('/bookAppointments', methods=['POST', 'GET'], strict_slashes=False)
def book_appointment():
    """to post appointment to db"""
    data = request.get_json()
    if data:
        data['patient_email'] = session['email']


        response = requests.post(f'http://localhost:5000/api/v1/appointment/post_appointment', json=data)
        if response.status_code == 201:
            msg = "appointment requested successfully"
        else:
            msg = "Couldn't request appointment"

        return jsonify({'msg' : msg}), response.status_code

@web.route('/updateAppointment/', methods=['PUT'], strict_slashes=False)
def update_appointments():
    """service to update appointments"""
    print("fn")
    data = request.get_json()
    data['approved'] = 'approved' if data['approved'] == 'approve' else 'declined'

    if data:
        # print(data)
        response = requests.put(f'http://localhost:5000/api/v1/appointment/put_appointment/{data.get('id')}', json=data)
        # print(response._content)
        appointment = requests.get(f'http://localhost:5000/api/v1/appointment/{data.get('id')}')
        # print(appointment._content)
    else:
        print('no')

    return jsonify({'msg': 'got data'})

if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
