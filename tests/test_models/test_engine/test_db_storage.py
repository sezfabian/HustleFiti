#!/usr/bin/env python3
import unittest
from datetime import datetime
from models.user import User
from models import storage

class Teststorage(unittest.TestCase):

    def setUp(self):
        # Set up test data
        self.user_data = {
            "email": "test2@example.com",
            "hashed_password": "password123",
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": datetime(1990, 1, 1),
            "gender": "Male",
            "phone_number": "4234567890",
            "user_image_path": "/path/to/image.jpg",
            "user_video_path": "/path/to/video.mp4",
            "user_banner_path": "/path/to/banner.jpg",
            "is_admin": False,
            "is_active": True,
            "is_verified": False,
        }

    def test_db_storage_add(self):
        count = storage.count()

        # Create a user object
        user2 = User(**self.user_data)

        # Add the user to the storage
        storage.delete_all()
        storage.new(user2)
        storage.save()


        # Assert that the retrieved user matches the original data
        self.assertEqual(storage.count(), count + 1)

        # Clean up: Delete the user from the storage
        storage.delete(user2)
        storage.save()

        # Assert that the user was deleted
        self.assertEqual(storage.count(), count)

    def test_db_storage_get(self):
        # User object creation and storage
        storage.delete_all()
        count = storage.count()
        user = User(**self.user_data)
        storage.new(user)
        storage.save()

        # Retrieve the user from the storage
        user_dict = user.to_dict()
        user_retrieved = storage.get(User, user_dict["id"])

        # Assert that the retrieved user matches the original data
        self.assertEqual(user_retrieved.email, self.user_data["email"])
        self.assertEqual(user_retrieved.first_name, self.user_data["first_name"])
        self.assertEqual(user_retrieved.last_name, self.user_data["last_name"])
        self.assertEqual(user_retrieved.user_image_path, self.user_data["user_image_path"])
        self.assertEqual(user_retrieved.user_video_path, self.user_data["user_video_path"])
        self.assertEqual(user_retrieved.user_banner_path, self.user_data["user_banner_path"])
        self.assertEqual(user_retrieved.is_admin, self.user_data["is_admin"])
        self.assertEqual(user_retrieved.is_active, self.user_data["is_active"])
        self.assertEqual(user_retrieved.is_verified, self.user_data["is_verified"])

        # Clean up: Delete the user from the storage
        storage.delete(user_retrieved)
        storage.save()


if __name__ == '__main__':
    unittest.main()
