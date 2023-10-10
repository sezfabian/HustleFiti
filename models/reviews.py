#!/usr/bin/env python3
"""
This module defines the reviews classes
"""
from sqlalchemy import Column, String, DateTime, Boolean, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import Base, BaseModel


class ServiceReview(BaseModel):
    """
    Implements the ServiceReview class
    """
    __tablename__ = 'service_reviews'

    user_id = Column(String(45), ForeignKey('users.id'), nullable=False)
    contract_id = Column(String(45), ForeignKey('contracts.id'), nullable=False)
    service_id = Column(String(45), ForeignKey('services.id'), nullable=False)
    rating = Column(DECIMAL(10, 2), nullable=False)
    comment = Column(String(255))

    # Define __init__ method with super class
    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)


class ClientReview(BaseModel):
    """
    Implements the ClientReview class
    """
    __tablename__ = 'client_reviews'

    contract_id = Column(String(45), ForeignKey('contracts.id'), nullable=False)
    user_id = Column(String(45), ForeignKey('users.id'), nullable=False)
    rating = Column(DECIMAL(10, 2), nullable=False)
    comment = Column(String(255))

    # Define __init__ method with super class
    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)