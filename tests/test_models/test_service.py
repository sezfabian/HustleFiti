#!/usr/bin/env python3
import unittest
from datetime import datetime
from models.user import User
from models.service import Service, ServiceCategory, PricePackage
from models import storage

class TestServiceCategory(unittest.TestCase):

    def setUp(self):
        # Set up test data for ServiceCategory class
        self.category_data = {
            "name": "Test Category",
            "sub_categories": "Subcategory 1, Subcategory 2",
        }

    def test_category_creation(self):
        # Test ServiceCategory object creation and storage
        storage.delete_all()
        count = storage.count(ServiceCategory)
        category = ServiceCategory(**self.category_data)
        storage.new(category)
        storage.save()

        # Retrieve the category from the storage
        category_dict = category.to_dict()
        category_retrieved = storage.get(ServiceCategory, category_dict["id"])

        # Assert that the retrieved category matches the original data
        self.assertEqual(category_retrieved.name, self.category_data["name"])
        self.assertEqual(category_retrieved.sub_categories, self.category_data["sub_categories"])
        self.assertEqual(storage.count(ServiceCategory), count + 1)

        # Clean up: Delete the category from the storage
        storage.delete(category_retrieved)
        storage.save()


class TestService(unittest.TestCase):
    
    def setUp(self):
        # Set up test data for Service class
        # Set up test data for ServiceCategory class
        # Set up test data
        self.user_data = {
            "email": "test@example.com",
            "hashed_password": "password123",
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": datetime(1990, 1, 1),
            "user_image_path": "/path/to/image.jpg",
            "user_video_path": "/path/to/video.mp4",
            "user_banner_path": "/path/to/banner.jpg",
            "is_admin": True,
            "is_active": True,
            "is_verified": True,
        }

        self.category_data = {
            "name": "Test Category",
            "sub_categories": "Subcategory 1, Subcategory 2",
        }

    def test_service_creation(self):
        # Test Service object creation and storage
        storage.delete_all()
        count = storage.count(Service)
        user = User(**self.user_data)
        storage.new(user)
        category = ServiceCategory(**self.category_data)
        storage.new(category)
        service_data = {
            "name": "Test Service",
            "description": "Test Service Description",
            "user_id": user.id,
            "service_category_id": category.id,
            "image_paths": "/path/to/image.jpg",
            "video_paths": "/path/to/video.mp4",
            "banner_paths": "/path/to/banner.jpg",
            "is_verified": True
        }
        service = Service(**service_data)
        storage.new(service)
        storage.save()

        # Retrieve the service from the storage
        service_dict = service.to_dict()
        service_retrieved = storage.get(Service, service_dict["id"])
        
        # Assert that the retrieved service matches the original data
        self.assertEqual(service_retrieved.name, service_data["name"])
        self.assertEqual(service_retrieved.description, service_data["description"])
        self.assertEqual(service_retrieved.user_id, service_data["user_id"])
        self.assertEqual(service_retrieved.service_category_id, service_data["service_category_id"])
        self.assertEqual(service_retrieved.image_paths, service_data["image_paths"])
        self.assertEqual(service_retrieved.video_paths, service_data["video_paths"])
        self.assertEqual(service_retrieved.banner_paths, service_data["banner_paths"])
        self.assertEqual(service_retrieved.is_verified, service_data["is_verified"])

        # Clean up: Delete the service from the storage
        storage.delete(service_retrieved)
        storage.delete(user)
        storage.delete(category)
        storage.save()
