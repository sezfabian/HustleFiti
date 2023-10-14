#!/usr/bin/env python3
"""
This module defines the contracts class
"""
from sqlalchemy import Column, String, DateTime, Boolean, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import Base, BaseModel
from models.reviews import ServiceReview, ClientReview
from model.payment import Payment
from flaskapp.app.extensions import db

class Contract(BaseModel, db.Model):
    """
    Implements the Contract class
    """
    __tablename__ = 'contracts'
    __table_args__ = {'extend_existing': True}


    user_id = db.Column(String(45), ForeignKey('users.id'), nullable=False)
    service_id = db.Column(String(45), ForeignKey('services.id'), nullable=False)
    location = db.Column(String(45), nullable=False)
    duration = db.Column(String(45))
    price_package_id = db.Column(String(45), ForeignKey('price_packages.id'), nullable=False)
    total_amount = db.Column(DECIMAL(10, 2))
    contract_start_date = db.Column(DateTime)
    contract_end_date = db.Column(DateTime)
    contract_status = db.Column(String(45), nullable=False)
    paid_amount = db.Column(DECIMAL(10, 2), nullable=False)

    # Define relationships
    contract_service_review = relationship('ServiceReview', backref='contracts')
    contract_client_review = relationship('ClientReview', backref='contracts')
    contract_payments = relationship('Payment', backref='contracts')

    # Define __init__ method with super class
    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
