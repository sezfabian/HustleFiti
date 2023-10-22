#!/usr/bin/env python3
from sqlalchemy import Column, String, DateTime, Boolean, Integer, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import Base, BaseModel


class User(BaseModel):
    """
    Implements the User class
    """
    __tablename__ = 'users'

    email = Column(String(45), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    username = Column(String(45), nullable=False, unique=True)
    date_of_birth = Column(DateTime, nullable=False)
    gender = Column(String(45), nullable=False)
    phone_number = Column(String(45))
    user_image_path = Column(String(255))
    user_video_path = Column(String(255))
    user_banner_path = Column(String(255))
    is_admin = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))
    verification_token = Column(String(20))
    no_of_ratings = Column(Integer, default=0)
    average_rating = Column(DECIMAL(10, 2), default=0)


    # Define relationships
    services = relationship('Service', back_populates='user')
    user_contracts = relationship('Contract', backref='users')
    user_payments = relationship('Payment', backref='users')
    user_client_reviews = relationship('ClientReview', backref='users')
    user_service_reviews = relationship('ServiceReview', backref='users')
    
    # Define __init__ method with super class
    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
