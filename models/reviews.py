#!/usr/bin/env python3
"""
This module defines the reviews classes
"""
from sqlalchemy import Column, String, DateTime, Boolean, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import Base, BaseModel
from flaskapp.app.extensions import db

class ServiceReview(BaseModel, db.Model):
    """
    Implements the ServiceReview class
    """
    __tablename__ = 'service_reviews'
    __table_args__ = {'extend_existing': True}

    user_id = db.Column(String(45), ForeignKey('users.id'), nullable=False)
    contract_id = db.Column(String(45), ForeignKey('contracts.id'), nullable=False)
    service_id = db.Column(String(45), ForeignKey('services.id'), nullable=False)
    rating = db.Column(DECIMAL(10, 2), nullable=False)
    comment = db.Column(String(255))

    # Define __init__ method with super class
    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)


class ClientReview(BaseModel, db.Model):
    """
    Implements the ClientReview class
    """
    __tablename__ = 'client_reviews'
    __table_args__ = {'extend_existing': True}

    contract_id = db.Column(String(45), ForeignKey('contracts.id'), nullable=False)
    user_id = db.Column(String(45), ForeignKey('users.id'), nullable=False)
    rating = db.Column(DECIMAL(10, 2), nullable=False)
    comment = db.Column(String(255))

    # Define __init__ method with super class
    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
