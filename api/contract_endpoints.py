from fastapi import APIRouter, HTTPException, Depends, Cookie, Path
from fastapi.responses import JSONResponse
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict
from models import storage
from models.user import User
from models.service import ServiceCategory, Service, PricePackage
from models.contract import Contract

contract_router = APIRouter()

class ContractCreate(BaseModel):
    service_id: str
    location: str
    map_link: Optional[str] = None
    duration: Optional[str] = None
    price_package_id: str
    total_amount: Optional[float] = None
    contract_start_date: Optional[str] = None
    contract_end_date: Optional[str] = None
    contract_status: Optional[str] = None
    paid_amount: Optional[float] = None

class ContractUpdate(BaseModel):
    service_id: Optional[str] = None
    location: Optional[str] = None
    map_link: Optional[str] = None
    duration: Optional[str] = None
    price_package_id: Optional[str] = None
    total_amount: Optional[float] = None
    contract_start_date: Optional[str] = None
    contract_end_date: Optional[str] = None
    contract_status: Optional[str] = None
    paid_amount: Optional[float] = None

# create a contract
@contract_router.post("/create", response_model=dict)
async def create_contract(contract_data: ContractCreate, user_id: str = None):
    user = storage.find_by(User, **{"id": user_id})
    if user is None:
        raise HTTPException(status_code=403, detail="User not logged in")

    try:
        contract_data_dict = contract_data.dict()
        contract_data_dict["user_id"] = user_id
        contract = Contract(**contract_data_dict)
        storage.new(contract)
        storage.save()
        return {"message": "new contract initiated successfully", "contract": contract.to_dict()}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# update contract
@contract_router.put("/update/{contract_id}", response_model=dict)
async def update_contract(contract_id: str, contract_data: ContractUpdate, user_id: str = None):
    user = storage.find_by(User, **{"id": user_id})
    if user is None:
        raise HTTPException(status_code=403, detail="User not logged in")

    contract = storage.find_by(Contract, **{"id": contract_id})
    if contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")

    try:
        contract_data_dict = contract_data.dict()
        storage.update(contract, **contract_data_dict)
        storage.save()
        contract = storage.find_by(Contract, **{"id": contract_id})
        return {"message": "Contract updated successfully", "contract": contract.to_dict()}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
