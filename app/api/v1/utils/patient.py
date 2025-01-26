#!/usr/bin/python3
"""
defines a the api endppoints for the patient class
"""
from app.models.patient import Patient
from app.models import storage
from app.api.v1.utils import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from

@app_views.route('/patient', methods=['GET'], strict_slashes=False)
@swag_from('documentation/patient/get_patient.yml', methods=['GET'])
def get_patients():
    """method to get all patients data from db"""
    all_patients = storage.all(Patient).values()
    list_patients = []
    for patient in all_patients:
        list_patients.append(patient.to_dict())
    return jsonify(list_patients)

@app_views.route('/patient/patient_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/patient/get_patients.yml', methods=['GET'])
def get_patient(patient_id):
    """method to get patient based off of id"""
    patient = storage.get(Patient, patient_id)
    if not patient:
        abort(404)

    return jsonify(patient.to_dict())

@app_views.route('/patient/get_patient_by_email/<patient_email>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/patient/get_patients_by_email.yml', methods=['GET'])
def get_patient_by_email(patient_email):
    """get patient by email"""
    try:
        print("getting")
        patient = storage.get_patient_by_email(patient_email)
        if patient:
            return jsonify({
                'first_name': patient.first_name,
                'last_name': patient.last_name,
                'id': patient.id,
                'email': patient.email,
                'tel': patient.tel,
                'role': patient.role,
                'pCode': patient.password,
                'age': patient.age
            })
        else:
            return jsonify({ 'email': patient_email}), 404
    except Exception as e:
        return jsonify({"something":e})


@app_views.route('/patient/del/<patient_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/patient/del_patient.yml', methods=['DELETE'])
def del_patient(patient_id):
    """delete individual patient based of off id"""
    patient = storage.get(Patient, patient_id)
    print("getting")
    if not patient:
        abort(404)

    storage.delete(patient)
    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('/patient/post_patient', methods=['POST'], strict_slashes=False)
@swag_from('documentation/patient/post_patient.yml', methods=['POST'])
def post_patient():
    """method to create patient to db"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()
    instance = Patient(**data)
    instance.save()
    return make_response(jsonify({"Created" : "success"}), 201)

@app_views.route('/patient/<patient_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/patient/put_patient.yml', methods=['PUT'])
def put_patient(patient_id):
    """update patient"""
    patient = storage.get(Patient, patient_id)

    if not patient:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(patient, key, value)
    storage.save()
    return make_response(jsonify(patient.to_dict()), 200) 
