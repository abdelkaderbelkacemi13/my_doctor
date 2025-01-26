#!/usr/bin/python3
"""
defines a the api endppoints for the user class
"""
from app.models.appointments import Appointment
from app.models import storage
from app.api.v1.utils import app_views
from flask import abort, jsonify, make_response, request, session
from flasgger.utils import swag_from

@app_views.route('/appointment', methods=['GET'], strict_slashes=False)
@swag_from('documentation/appointment/get_user.yml', methods=['GET'])
def get_appointments():
    """method to get all users data from db"""
    all_appointments = storage.all(Appointment).values()
    list_appointments = []
    for appointment in all_appointments:
        list_appointments.append(appointment.to_dict())
    return jsonify(list_appointments)

@app_views.route('/appointment/<appointment_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/appointment/get_appointment.yml', methods=['GET'])
def get_appointment_by_id(appointment_id):
    """method to get appointment based off of id"""
    appointment = storage.get(Appointment, appointment_id)
    if not appointment:
        abort(404)

    return jsonify(appointment.to_dict())

@app_views.route('/appointment/get_appointment_by_doctor_email/<doctor_email>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get_users_by_doctor_email.yml', methods=['GET'])
def get_appointment_by_doctor_email(doctor_email):
    """get appointment by doctor email"""
    doctor_appointments = []
    try:
        appointments = storage.get_appointment_by_doctor_email(doctor_email)
        print("getting appointment")
        if appointments:
            for appointment in appointments:
                doctor_appointments.append(appointment.to_dict())
            
            return jsonify(doctor_appointments)
        else:
            return jsonify({ 'email': doctor_email}), 404
    except Exception as e:
        return jsonify({"something":e})

@app_views.route('/appointment/get_appointment_by_patient_email/<patient_email>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get_users_by_doctor_email.yml', methods=['GET'])
def get_appointment_by_patient_email(patient_email):
    """get appointment by patient email"""
    patient_appointment = []
    try:
        appointments = storage.get_appointment_by_patient_email(patient_email)
        if appointments:
            for appointment in appointments:
                patient_appointment.append(appointment.to_dict())
            
            return jsonify(patient_appointment)
        else:
            return jsonify({ 'email': patient_email}), 404
    except Exception as e:
        return jsonify({"something":e})

@app_views.route('/appointment/del/<appointment_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/appointment/del_appointment.yml', methods=['DELETE'])
def del_appointment(appointment_id):
    """delete individual appointment based of off id"""
    appointment = storage.get(Appointment, appointment_id)
    print("getting")
    if not appointment:
        abort(404)

    storage.delete(appointment)
    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('/appointment/post_appointment', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/post_appointment.yml', methods=['POST'])
def post_appointment():
    """method to create appointment to db"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    
    data = request.get_json()
    data['approved'] = 'pending'
    print(data)

    if 'doctor_email' not in data:
        abort(400, description="Missing doctor_email")
    if 'patient_email' not in data:
        abort(400, description="Missing patient_email")
    if 'date' not in data:
        abort(400, description="Missing date")

    
    print(data)
    instance = Appointment(**data)
    instance.save()
    return make_response(jsonify({"Created" : "success"}), 201)

@app_views.route('/appointment/put_appointment/<appointment_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/appointment/put_appointment.yml', methods=['PUT'])
def put_appointment(appointment_id):
    """update user"""
    print("updating")
    appointment = storage.get(Appointment, appointment_id)
    print(appointment)
    
    if not appointment:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'patient_email', 'doctor_email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            # print(key, value)
            setattr(appointment, key, value)
    storage.save()
    print('updated')
    # appointment = storage.get(Appointment, appointment_id)
    # print(appointment)
    return make_response(jsonify(appointment.to_dict()), 200) 
