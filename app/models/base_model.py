#!/usr/bin/python3
"""
contains the default definition of all data models
it is to be used by all subsequent files in this parent folder
has functions like:
    save(self): saves data to db
    to_dict(self): converts obj to dict
    delete(self): deletes data from DB
    __str__(self): prints string representation of class
"""
from datetime import datetime
from app import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid

if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object

time = "%Y-%m-%dT%H:%M:%S.%f"

class BaseModel:
    """
    class definition of basemodel data model
    """
    if models.storage_t == "db":
        id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__ (self, *args, **kwargs):
        """
        constructor method to initialize class attributes from 
        arguments passed during class instantiation
        Args:
            *args: singular argument
            **kwargs: json argument
        """
        if kwargs: # if json object is passed
            for key, value in kwargs: # loop through kwargs and create the attr
                if key != "__class__":
                    setattr(self, key, value)
            # update the attr individually based on presence
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow
            if kwargs.get("updated_at", None) and type(self.created_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else: # update if nothing was passed
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow
            self.updated_at = self.created_at # so both match by default

    def save(self):
        """
        saves the class object to db 
        """
        # update updated_at attr
        self.update_at = datetime.utcnow
        # call methods in storage to save
        models.storage.new(self)
        models.storage.save()

    def __str__(self):
        """print string representation """
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                         self.__dict__)

    def to_dict(self):
        """return dict representation of object"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]

        return (new_dict)

    def delete(self):
        """delete the class instance"""
        app.models.storage.delete(self)
