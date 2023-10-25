#!/usr/bin/python3
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from uuid import uuid4
from datetime import datetime
import models


Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(String(45), primary_key=True, default=str(uuid4()), unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel.
        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """

        self.id = str(uuid4())
        self.created_at = self.updated_at = datetime.utcnow()
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)

    def save(self):
        """Update updated_at with the current datetime."""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Return a dictionary representation of the BaseModel instance.
        Includes the key/value pair __class__ representing
        the class name of the object.
        """
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = str(type(self).__name__)
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        my_dict.pop("_sa_instance_state", None)
        return my_dict

    def delete(self):
        """Delete the current instance from storage."""
        models.storage.delete(self)
    
    def update(self, **kwargs):
        """Update an instance of the class object.
        Args:
            **kwargs (dict): Key/value pairs of attributes to update.
        """
        for key, value in kwargs.items():
            if key == "created_at" or key == "updated_at":
                value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
            if key != "__class__":
                setattr(self, key, value)

    def __str__(self):
        """Return the print/str representation of the BaseModel instance."""
        dictString = self.__dict__.copy()
        dictString.pop("_sa_instance_state", None)
        return "[{}] ({}) {}".format(type(self).__name__, self.id, dictString)
