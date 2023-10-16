#!/usr/bin/env python3
"""
This module defines the services class and related models
ServiceCategories and PricePackages
"""
from sqlalchemy import Column, String, DateTime, Boolean, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import Base, BaseModel
from flaskapp.app.extensions import db

class ServiceCategory(BaseModel, db.Model):
    """
    Implements the ServiceCategory class
    """
    __tablename__ = 'service_categories'
    __table_args__ = {'extend existing': True}

    name = db.Column(String(45), nullable=False)
    sub_categories = db.Column(String(255))

    # Define relationships
    category_services = relationship('Service', backref='service_categories')


class Service(BaseModel, db.Model):
    """
    Implements the Service class
    """
    __tablename__ = 'services'
    __table_args__ = {'extend existing': True}

    name = db.Column(String(45), nullable=False)
    description = db.Column(String(255))
    user_id = db.Column(String(45), ForeignKey('users.id'), nullable=False)
    service_category_id = db.Column(String(45), ForeignKey('service_categories.id'))
    sub_category = db.Column(String(45))
    image_paths = db.Column(String(255))
    video_paths = db.Column(String(255))
    banner_paths = db.Column(String(255))
    is_verified = db.Column(Boolean, nullable=False)

    # Define relationships
    user = relationship('User', back_populates='services')
    service_price_packages = relationship('PricePackage', backref='services')
    service_contracts = relationship('Contract', backref='services')
    service_reviews = relationship('ServiceReview', backref='services')

    # Define __init__ method with super class
    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)


class PricePackage(BaseModel, db.Model):
    """
    Implements the PricePackage class
    """
    __tablename__ = 'price_packages'
    __table_args__ = {'extend existing': True}

    name = db.Column(String(45), nullable=False)
    service_id = db.Column(String(45), ForeignKey('services.id'), nullable=False)
    description = db.Column(String(255), nullable=False)
    price = db.Column(DECIMAL(10, 2), nullable=False)
    duration = db.Column(String(45))

    # Define relationships
    package_contracts = relationship('Contract', backref='price_packages')

    # Define __init__ method with super class
    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
