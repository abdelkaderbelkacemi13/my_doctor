#!/usr/bin/python3
"""
Contains the class DBStorage
"""

from app.models.appointments import Appointment
from app.models.base_model import Base
from app.models.doctor import Doctor
from app import models
from app.models.patient import Patient
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Doctor": Doctor, "Appointment": Appointment, "Patient": Patient}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        MY_APPOINTMENT_MYSQL_USER = getenv('MY_APPOINTMENT_MYSQL_USER')
        MY_APPOINTMENT_MYSQL_PWD = getenv('MY_APPOINTMENT_MYSQL_PWD')
        MY_APPOINTMENT_MYSQL_HOST = getenv('MY_APPOINTMENT_MYSQL_HOST')
        MY_APPOINTMENT_MYSQL_DB = getenv('MY_APPOINTMENT_MYSQL_DB')
        MY_APPOINTMENT_ENV = getenv('MY_APPOINTMENT_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(MY_APPOINTMENT_MYSQL_USER,
                                             MY_APPOINTMENT_MYSQL_PWD,
                                             MY_APPOINTMENT_MYSQL_HOST,
                                             MY_APPOINTMENT_MYSQL_DB))
        if MY_APPOINTMENT_ENV == "test":
            Base.metadata.drop_all(self.__engine)

        print(f"Initializing DBStorage with: user={MY_APPOINTMENT_MYSQL_USER}, host={MY_APPOINTMENT_MYSQL_HOST}, db={MY_APPOINTMENT_MYSQL_DB}")

        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def get_patient_by_email(self, email):
        """ Retrieve a user by their email """
        try:
            return self.__session.query(Patient).filter_by(email=email).first()
        except Exception as e:
            print(f"Error retrieving patient by email: {e}")
        return None
    
    def get_appointment_by_patient_email(self, email):
        """retrieve get_appointment_by_patient_email"""
        try:
            return self.__session.query(Appointment).filter_by(patient_email=email).all()
        except Exception as e:
          print(f"Error retrieving patients appointments:{e}")
        return None


    def get_doctor_by_email(self, email):
        """ Retrieve a user by their email """
        try:
            return self.__session.query(Doctor).filter_by(email=email).first()
        except Exception as e:
            print(f"Error retrieving doctor by email: {e}")
        return None
    
    def get_doctor_by_specialization(self, specialization):
        """ Retrieve a doctor by their specialization """
        try:
            return self.__session.query(Doctor).filter_by(specialization=specialization).all()
        except Exception as e:
            print(f"Error retrieving doctor by email: {e}")
        return None
        
    def get_appointment_by_doctor_email(self, email):
        """retrieve get_appointment_by_doctor_email"""
        try:
            print(email)
            return self.__session.query(Appointment).filter_by(doctor_email=email).all()
        except Exception as e:
          print(f"Error retrieving doctors appointment:{e}")
        return None

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        print("created")
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count
