#!/usr/bin/python3
"""
defines a class for the doctor inherits from BaseModel and Base
"""
from app import models
from app.models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5
import uuid


class Doctor(BaseModel, Base):
    """
    a class doctor that extends BaseModel class
    """
    if models.storage_t == 'db':
        __tablename__ = 'doctors'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=True)
        specialization = Column(String(128), nullable=False)
        id_number = Column(String(128), nullable=True)
        tel = Column(String(128), nullable=True)
        role = Column(String(128), nullable=True)
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
        age=""
        specialization=""
        role = ""
        tel = ""

    def __init__(self, email, password, first_name, specialization, phone_number=None, id_number=None, last_name=None):
        """constructor"""
        self.id = str(uuid.uuid4())
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.id_number = id_number
        self.specialization = specialization
        self.tel = phone_number
        self.role = "doctor"

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
