from fastapi import APIRouter, HTTPException, Depends, Cookie, Path
from fastapi.responses import JSONResponse
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict
from models import storage
from models.user import User
from models.service import ServiceCategory, Service, PricePackage
from models.contract import Contract
from models.payment import Payment

payment_router = APIRouter()

class PaymentCreate(BaseModel):
    amount: float
    payment_method: str
    transaction_id: str
    phone_number: Optional[str] = None
    email: Optional[str] = None
    account_number: Optional[str] = None
    bank: Optional[str] = None
    payment_status: Optional[str] = None

# create a new payment
@payment_router.post("/payment/{contract_id}", response_model=dict)
async def create_payment(contract_id: str, payment_data: PaymentCreate, session_id: str = Cookie(None), encrypted_session_id: Optional[str] = None):
    if encrypted_session_id:
        session_id = encrypted_session_id.rstrip('*')
  
    if session_id is None:
        raise HTTPException(status_code=403, detail="User not logged in")
    
    user = storage.find_by(User, **{"session_id": session_id})
    if user is None:
        raise HTTPException(status_code=403, detail="User session expired")

    payment_data_dict = payment_data.dict()
    payment_data_dict["user_id"] = user.to_dict()["id"]
    payment_data_dict["contract_id"] = contract_id

    try:
        payment = Payment(**payment_data_dict)
        storage.new(payment)
        storage.save()
        return {"message": "Payment created successfully", "payment": payment.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get payment by id
@payment_router.get("/payment/{payment_id}", response_model=dict)
async def get_payment(payment_id: str, session_id: str = Cookie(None)):
    if session_id is None:
        raise HTTPException(status_code=403, detail="User not logged in")
    
    user = storage.find_by(User, **{"session_id": session_id})
    if user is None:
        raise HTTPException(status_code=403, detail="User session expired")

    payment = storage.find_by(Payment, **{"id": payment_id})
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment.to_dict()

# Get payments by user  
@payment_router.get("/payments", response_model=list)
async def get_payments(session_id: str = Cookie(None), encrypted_session_id: Optional[str] = None):
    if encrypted_session_id:
        session_id = encrypted_session_id.rstrip('*')

    if session_id is None:
        raise HTTPException(status_code=403, detail="User not logged in")
    
    user = storage.find_by(User, **{"session_id": session_id})
    
    if user is None:
        raise HTTPException(status_code=403, detail="User session expired")
    
    try:
        payments = storage.find_all(Payment)
        payments_list = [payment.to_dict() for payment in payments if payment.to_dict()["user_id"] == user.to_dict()["id"]]
        return payments_list
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Get all payments by contract
@payment_router.get("/payments/{contract_id}", response_model=list)
async def get_payments_by_contract(contract_id: str, session_id: str = Cookie(None), encrypted_session_id: Optional[str] = None):
    if encrypted_session_id:
        session_id = encrypted_session_id.rstrip('*')

    if session_id is None:
        raise HTTPException(status_code=403, detail="User not logged in")
    
    user = storage.find_by(User, **{"session_id": session_id})
    if user is None:
        raise HTTPException(status_code=403, detail="User session expired")
    
    contract = storage.find_by(Contract, **{"id": contract_id})

    if contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")

    if user.to_dict()["is_admin"] != False:
        if user.to_dict()["id"] != contract.to_dict()["user_id"]:
            raise HTTPException(status_code=403, detail="Unauthorized")

    payments = storage.find_all(Payment, **{"contract_id": contract_id})
    payments_list = [payment.to_dict() for payment in payments]
    return payments_list

# delete payment records
@payment_router.delete("/payment/{payment_id}", response_model=dict)
async def delete_payment(payment_id: str, session_id: str = Cookie(None), encrypted_session_id: Optional[str] = None):
    if encrypted_session_id:
        session_id = encrypted_session_id.rstrip('*')

    if session_id is None:
        raise HTTPException(status_code=403, detail="User not logged in")
    
    user = storage.find_by(User, **{"session_id": session_id})

    if user is None:
        raise HTTPException(status_code=403, detail="User session expired")
    
    if user.to_dict()["is_admin"] != False:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    payment = storage.find_by(Payment, **{"id": payment_id})
    
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    try:
        storage.delete(payment)
        storage.save()
        return {"message": "Payment deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))