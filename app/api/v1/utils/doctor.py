#!/usr/bin/python3
"""
defines a the api endppoints for the doctor class
"""
from app.models.doctor import Doctor
from app.models import storage
from app.api.v1.utils import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from

@app_views.route('/doctors', methods=['GET'], strict_slashes=False)
@swag_from('documentation/doctor/get_doctor.yml', methods=['GET'])
def get_doctors():
    """method to get all doctors data from db"""
    print("getting")
    all_doctors = storage.all(Doctor).values()
    list_doctors = []
    for doctor in all_doctors:
        list_doctors.append(doctor.to_dict())
    return jsonify(list_doctors)

@app_views.route('/doctor/<doctor_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/doctor/get_doctors.yml', methods=['GET'])
def get_doctor(doctor_id):
    """method to get doctor based off of id"""
    doctor = storage.get(Doctor, doctor_id)
    if not doctor:
        abort(404)

    return jsonify(doctor.to_dict())

@app_views.route('/doctor/get_doctor_by_email/<doctor_email>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/doctor/get_doctors_by_email.yml', methods=['GET'])
def get_doctor_by_email(doctor_email):
    """get doctor by email"""
    try:
        print("getting")
        doctor = storage.get_doctor_by_email(doctor_email)
        if doctor:
            return jsonify({
                'first_name':doctor.first_name,
                'last_name':doctor.last_name,
                'id': doctor.id,
                'email': doctor.email,
                'tel': doctor.tel,
                'role': doctor.role,
                'pCode': doctor.password,
                'specialization': doctor.specialization
            })
        else:
            return jsonify({ 'email': doctor_email}), 404
    except Exception as e:
        return jsonify({"something":e})


@app_views.route('/doctor/get_doctor_by_specialization/<specialization>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/doctor/get_doctors_by_specialization.yml', methods=['GET'])
def get_doctor_by_specialization(specialization):
    """get doctor by email"""
    doctors_list = []
    try:
        doctors = storage.get_doctor_by_specialization(specialization)
        if doctors:
            for doctor in doctor:
                doctors_list.append(
                   doctor.to_dict())
            return jsonify(doctors_list)
        else:
            return jsonify({ 'specialization': specialization}), 404
    except Exception as e:
        return jsonify({"something":e})


@app_views.route('/doctor/del/<doctor_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/doctor/del_doctor.yml', methods=['DELETE'])
def del_doctor(doctor_id):
    """delete individual doctor based of off id"""
    doctor = storage.get(Doctor, doctor_id)
    print("getting")
    if not doctor:
        abort(404)

    storage.delete(doctor)
    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('/doctor/post_doctor', methods=['POST'], strict_slashes=False)
@swag_from('documentation/doctor/post_doctor.yml', methods=['POST'])
def post_doctor():
    """method to create doctor to db"""
    print("got data")
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()
    instance = Doctor(**data)
    instance.save()
    return make_response(jsonify({"Created" : "success"}), 201)

@app_views.route('/doctor/<doctor_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/doctor/put_doctor.yml', methods=['PUT'])
def put_doctor(doctor_id):
    """update doctor"""
    doctor = storage.get(Doctor, doctor_id)

    if not doctor:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(doctor, key, value)
    storage.save()
    return make_response(jsonify(doctor.to_dict()), 200) 
