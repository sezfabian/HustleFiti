#!/usr/bin/python3
"""
How to store data in the database
"""

# Import necessary modules and classes
from models import storage
from models.service import ServiceCategory

# Define service category data
service_category_data = {
    "name": "General",
    "sub_categories": "All",
}


category = ServiceCategory(**service_category_data)

# Store the user data in the database
storage.new(category)
storage.save()