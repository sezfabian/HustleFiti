#!/usr/bin/python3
"""
How to store data in the database
"""

# Import necessary modules and classes
from models import storage
from datetime import datetime
from models.user import User

# Define user data dictionary and create a User instance
user_data = {
    "email": "lawrence@example.com",
    "hashed_password": "password123",
    "first_name": "Lawrence",
    "last_name": "Job",
    "date_of_birth": datetime(1990, 1, 1),
    "user_image_path": "/path/to/image.jpg",
    "user_video_path": "/path/to/video.mp4",
    "user_banner_path": "/path/to/banner.jpg",
    "is_admin": True,
    "is_active": True,
    "is_verified": True,
}

user = User(**user_data)

# Store the user data in the database
storage.new(user)
storage.save()
