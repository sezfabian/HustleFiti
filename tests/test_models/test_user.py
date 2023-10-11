#!/usr/bin/python3
"""
Contains the TestUserDocs and TestUser classes
"""

from datetime import datetime
import inspect
import models
from models import user
from models.base_model import BaseModel
import pep8
import unittest
User = user.User


class TestUserDocs(unittest.TestCase):
    """Tests to check the documentation and style of the User class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.user_f = inspect.getmembers(User, inspect.isfunction)

    def test_pep8_conformance_user(self):
        """Test that models/user.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/user.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_user(self):
        """Test that tests/test_models/test_user.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_user.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_user_module_docstring(self):
        """Test for the user.py module docstring"""
        self.assertIsNot(user.__doc__, None,
                         "user.py needs a docstring")
        self.assertTrue(len(user.__doc__) >= 1,
                        "user.py needs a docstring")

    def test_user_class_docstring(self):
        """Test for the User class docstring"""
        self.assertIsNot(User.__doc__, None,
                         "User class needs a docstring")
        self.assertTrue(len(User.__doc__) >= 1,
                        "User class needs a docstring")

    def test_user_func_docstrings(self):
        """Test for the presence of docstrings in User methods"""
        for func in self.user_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestUser(unittest.TestCase):
    """Test the User class"""
    def test_is_subclass(self):
        """Test that User is a subclass of BaseModel"""
        user = User()
        self.assertIsInstance(user, BaseModel)
        self.assertTrue(hasattr(user, "id"))
        self.assertTrue(hasattr(user, "created_at"))
        self.assertTrue(hasattr(user, "updated_at"))

    def test_email_attr(self):
        """Test that User has an email attribute"""
        user = User()
        self.assertTrue(hasattr(user, "email"))
        self.assertEqual(user.email, "")

    def test_hashed_password_attr(self):
        """Test that User has a hashed_password attribute"""
        user = User()
        self.assertTrue(hasattr(user, "hashed_password"))
        self.assertEqual(user.hashed_password, "")

    def test_first_name_attr(self):
        """Test that User has a first_name attribute"""
        user = User()
        self.assertTrue(hasattr(user, "first_name"))
        self.assertEqual(user.first_name, "")

    def test_last_name_attr(self):
        """Test that User has a last_name attribute"""
        user = User()
        self.assertTrue(hasattr(user, "last_name"))
        self.assertEqual(user.last_name, "")

    def test_date_of_birth_attr(self):
        """Test that User has a date_of_birth attribute"""
        user = User()
        self.assertTrue(hasattr(user, "date_of_birth"))
        self.assertEqual(user.date_of_birth, datetime(1970, 1, 1))

    def test_user_image_path_attr(self):
        """Test that User has a user_image_path attribute"""
        user = User()
        self.assertTrue(hasattr(user, "user_image_path"))
        self.assertEqual(user.user_image_path, "")

    def test_user_video_path_attr(self):
        """Test that User has a user_video_path attribute"""
        user = User()
        self.assertTrue(hasattr(user, "user_video_path"))
        self.assertEqual(user.user_video_path, "")

    def test_user_banner_path_attr(self):
        """Test that User has a user_banner_path attribute"""
        user = User()
        self.assertTrue(hasattr(user, "user_banner_path"))
        self.assertEqual(user.user_banner_path, "")

    def test_is_admin_attr(self):
        """Test that User has an is_admin attribute"""
        user = User()
        self.assertTrue(hasattr(user, "is_admin"))
        self.assertEqual(user.is_admin, False)

    def test_is_active_attr(self):
        """Test that User has an is_active attribute"""
        user = User()
        self.assertTrue(hasattr(user, "is_active"))
        self.assertEqual(user.is_active, True)

    def test_is_verified_attr(self):
        """Test that User has an is_verified attribute"""
        user = User()
        self.assertTrue(hasattr(user, "is_verified"))
        self.assertEqual(user.is_verified, False)

    def test_to_dict_creates_dict(self):
        """
        Test that to_dict method creates a dictionary with proper attributes
        """
        u = User()
        new_d = u.to_dict()
        self.assertEqual(type(new_d), dict)
        for attr in ["id", "created_at", "updated_at", "email",
                     "hashed_password", "first_name", "last_name",
                     "date_of_birth", "user_image_path", "user_video_path",
                     "user_banner_path", "is_admin", "is_active",
                     "is_verified"]:
            self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """Test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        u = User()
        new_d = u.to_dict()
        self.assertEqual(new_d["__class__"], "User")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], u.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], u.updated_at.strftime(t_format))
