#!/usr/bin/python3
"""
defines a class for the user inherits from BaseModel and Base
"""
from app import models
from app.models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from hashlib import md5
import uuid


class Appointment(BaseModel, Base):
    """
    a class user that extends BaseModel class
    """
    if models.storage_t == 'db':
        __tablename__ = 'requested_appointment'
        patient_email = Column(String(128), nullable=False)
        doctor_email = Column(String(128), nullable =False)
        doctors_specialization = Column(String(128), nullable=False)
        date = Column(String(128), nullable =False)
        approved = Column(String(128), nullable=False)
    else:
        patient_email = ""
        doctor_email = ""
        date = ""
        approved=""

    def __init__(self, patient_email, doctor_email, doctors_specialization, date, approved):
        """constructor"""
        self.id = str(uuid.uuid4())
        self.doctor_email = doctor_email
        self.patient_email = patient_email
        self.doctors_specialization = doctors_specialization
        self.date = date
        self.approved = approved

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
