#!/usr/bin/python3
"""
defines a class for the patient inherits from BaseModel and Base
"""
from app import models
from app.models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5
import uuid


class Patient(BaseModel, Base):
    """
    a class patient that extends BaseModel class
    """
    if models.storage_t == 'db':
        __tablename__ = 'patients'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        tel = Column(String(128), nullable=True)
        age = Column(String(128), nullable=True)
        role = Column(String(128), nullable=True)
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
        tel = ""
        age=""
        #specialization=""
        role = ""

    def __init__(self, email, password, first_name=None, last_name=None, age=None, phone_number=None):
        """constructor"""
        self.id = str(uuid.uuid4())
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.tel = phone_number
        self.role = "patient"
        self.age = age

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
