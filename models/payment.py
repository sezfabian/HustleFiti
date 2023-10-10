#!/usr/bin/env python3
"""
This module defines the contracts class
"""
from sqlalchemy import Column, String, DateTime, Boolean, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import Base, BaseModel


class Payment(BaseModel):
    """
    Implements the Payment class
    """
    __tablename__ = 'payments'

    user_id = Column(String(45), ForeignKey('users.id'), nullable=False)
    contract_id = Column(String(45), ForeignKey('contracts.id'), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_method = Column(String(45), nullable=False)
    transaction_id = Column(String(45), nullable=False)
    phone_number = Column(String(45))
    email = Column(String(45))
    account_number = Column(String(45))
    bank = Column(String(45))
    payment_status = Column(String(45), nullable=False)

    # Define __init__ method with super class
    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)