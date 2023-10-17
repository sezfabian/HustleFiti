import unittest
from models import storage
from models.user import User
from datetime import datetime
from models.engine.auth import Auth

class Teststorage(unittest.TestCase):

    def setUp(self):
        # Set up test data
        self.user_data = {
            "email": "test3@example.com",
            "password": "password123",
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

    def test_auth_register_user(self):
        # Register new user
        auth = Auth()
        user = auth.register_user(self.user_data)
        self.assertEqual(user.email, self.user_data["email"])

        # Clean up: Delete the user from the storage
        storage.delete(user)
        storage.save()
    
    def test_auth_valid_login(self):
        # Register new user
        auth = Auth()
        user = auth.register_user(self.user_data)

        # Check if login is valid
        self.assertTrue(auth.valid_login(self.user_data["email"], self.user_data["password"]))

        # Clean up: Delete the user from the storage
        storage.delete(user)
        storage.save()
    
    def test_auth_invalid_login(self):
        # Register new user
        auth = Auth()
        user = auth.register_user(self.user_data)

        # Check if login is valid
        self.assertFalse(auth.valid_login(self.user_data["email"], "invalid_password"))

        # Clean up: Delete the user from the storage
        storage.delete(user)
        storage.save()

    def test_create_session(self):
        # Register new user
        auth = Auth()
        user = auth.register_user(self.user_data)

        # Check if login is valid
        session_id = auth.create_session(self.user_data["email"])
        self.assertIsNotNone(session_id)

        # Retrieve the user from the storage
        user = auth._db.find_by(User, **{"email": self.user_data["email"]})
        self.assertIsNotNone(user)
        self.assertEqual(user.session_id, session_id)

        # Clean up: Delete the user from the storage
        storage.delete(user)
        storage.save()

    def test_delete_session(self):
        # Register new user
        auth = Auth()
        auth.register_user(self.user_data)

        # Check if login is valid
        auth = Auth()
        is_valid = auth.valid_login(self.user_data["email"], self.user_data["password"])
        if is_valid:
            session_id = auth.create_session(self.user_data["email"])
            self.assertIsNotNone(session_id)

            # Retrieve the user from the storage
            user_retrieved = auth._db.find_by(User, **{"email": self.user_data["email"]})
            self.assertIsNotNone(user_retrieved)
            self.assertEqual(user_retrieved.session_id, session_id)

        # delete the session
        user = auth._db.find_by(User, **{"email": self.user_data["email"]})
        auth.destroy_session(user.id)
        user = auth._db.find_by(User, **{"email": self.user_data["email"]})
        self.assertIsNone(user.session_id)

        # Clean up: Delete the user from the storage
        # Delete the user from the storage
        storage.delete(user)
        storage.save()

    def test_get_user_by_session_id(self):
        # Register new user
        auth = Auth()
        user = auth.register_user(self.user_data)

        # Create session
        session_id = auth.create_session(self.user_data["email"])
        self.assertIsNotNone(session_id)

        # Retrieve the user by session ID
        user = auth.get_user_from_session_id(session_id)
        self.assertEqual(user.email, self.user_data["email"])
        
        # Clean up: Delete the user from the storage
        storage.delete(user)
        storage.save()

if __name__ == '__main__':
    unittest.main