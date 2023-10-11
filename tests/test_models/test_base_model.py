#!/usr/bin/python3
"""
Contains unittest for the BaseModel
"""
import unittest
from models.base_model import BaseModel
import datetime
import json


class TestBaseModel(unittest.TestCase):
    def test_id(self):
        """Test that the id attribute is a string and not empty."""
        my_model = BaseModel()
        self.assertIsInstance(my_model.id, str)
        self.assertNotEqual(my_model.id, "")

    def test_created_at(self):
        """Test that created_at is a datetime object."""
        my_model = BaseModel()
        self.assertIsInstance(my_model.created_at, datetime.datetime)

    def test_updated_at(self):
        """Test that updated_at is a datetime object."""
        my_model = BaseModel()
        self.assertIsInstance(my_model.updated_at, datetime.datetime)

    def test_save(self):
        """Test that save updates the updated_at attribute."""
        my_model = BaseModel()
        original_updated_at = my_model.updated_at
        my_model.save()
        self.assertNotEqual(my_model.updated_at, original_updated_at)

    def test_to_dict(self):
        """Test the to_dict method."""
        my_model = BaseModel()
        my_model_dict = my_model.to_dict()

        self.assertIsInstance(my_model_dict, dict)
        self.assertIn("__class__", my_model_dict)
        self.assertIn("id", my_model_dict)
        self.assertIn("created_at", my_model_dict)
        self.assertIn("updated_at", my_model_dict)

    def test_str(self):
        """Test the __str__ method."""
        my_model = BaseModel()
        self.assertIsInstance(str(my_model), str)
        self.assertIn("[BaseModel] ({})".format(my_model.id), str(my_model))

    def test_from_dict(self):
        """Test creating a model instance from a dictionary."""
        data = {
            "id": "12345",
            "created_at": "2023-10-01T12:34:56.789",
            "updated_at": "2023-10-01T12:34:56.789"
        }
        my_model = BaseModel(**data)

        self.assertEqual(my_model.id, "12345")
        self.assertIsInstance(my_model.created_at, datetime.datetime)
        self.assertIsInstance(my_model.updated_at, datetime.datetime)
        self.assertEqual(my_model.created_at.isoformat(),
                         "2023-10-01T12:34:56.789")
        self.assertEqual(my_model.updated_at.isoformat(),
                         "2023-10-01T12:34:56.789")

    def test_delete(self):
        """Test the delete method."""
        my_model = BaseModel()
        my_model.save()
        my_model_id = my_model.id
        my_model.delete()
        self.assertIsNone(models.storage.get(BaseModel, my_model_id))


if __name__ == '__main__':
    unittest.main()
