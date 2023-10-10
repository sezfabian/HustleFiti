#!/usr/bin/python3
"""
class base model
"""

import datetime
import uuid
import models


class BaseModel:
    """
    BaseModel defines all common attributes/methods for other classes
    PUBLIC INSTANCE ATTRIBUTES:
    id: string - assign with a uuid when an instance is created
        uuid.uuid4(): generate a unique id and convert to a string
    created_at: datetime - assign with the current datetime when an instance
                is created
    updated_at: datetime - assign with the current datetime when an instance
                is created and will be updated every time an object changes
    __str__: should print : [<class name>] (self.id) <self.__dict__>
    PUBLIC INSTANCE METHODS:
    save(self): save method save object to file/db storage
    to_dict(self): convert to dictionary all key/values of the __dict__ instance
    """


    def __init__(self, *args, **kwargs):
        """initialize method of the class"""
        format = "%Y-%m-%dT%H:%M:%S.%f"
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.strptime(value, format))
                elif key == "__class__":
                    setattr(self, key, type(self))
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """str representation of the instance object class"""
        return "[{}]({}) {}".format(self.__class__.__name__,
                                    self.id,
                                    self.__dict__)


    def save(self):
        """
        updates the public instance attribute
        updated_at with current datetime
        """
        self.updated_at = datetime.now()
        model.storage.save()


    def to_dict(self):
        """
        Method creates dictionary representation for object
        type of our BaseModel
        Returns: a dictionary containing all key/values of __dict__ instance
        """
        new_dict = dict(self.__dict__)
        new_dict["__class__"] = type(self).__name__
        new_dict["created_at"] = new_dict["created_at"].isoformat()
        new_dict["updated_at"] = new_dict["updated_at"].isoformat()
        return new_dict
