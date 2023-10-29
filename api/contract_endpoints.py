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

class ContractUpdate(BaseModel):
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
async def create_contract(contract_data: ContractCreate, session_id: str = Cookie(None), encrypted_session_id: Optional[str] = None):
    if encrypted_session_id:
        session_id = encrypted_session_id.rstrip('*')

    if session_id is None:
        raise HTTPException(status_code=403, detail="User not logged in")

    user = storage.find_by(User, **{"session_id": session_id})
    if user is None:
        raise HTTPException(status_code=403, detail="User not logged in")

    try:
        contract_data_dict = contract_data.dict()
        contract_data_dict["user_id"] = user.to_dict()["id"]
        contract = Contract(**contract_data_dict)
        storage.new(contract)
        storage.save()
        return {"message": "new contract initiated successfully", "contract": contract.to_dict()}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# update contract
@contract_router.put("/update/{contract_id}", response_model=dict)
async def update_contract(contract_id: str, contract_data: ContractUpdate, session_id: str = Cookie(None), encrypted_session_id: Optional[str] = None):
    if encrypted_session_id:
        session_id = encrypted_session_id.rstrip('*')

    if session_id is None:
        raise HTTPException(status_code=403, detail="User not logged in")

    user = storage.find_by(User, **{"session_id": session_id})
    if user is None:
        raise HTTPException(status_code=403, detail="User not logged in")

    contract = storage.find_by(Contract, **{"id": contract_id})
    if contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    service = storage.find_by(Service, **{"id": contract.to_dict()["service_id"]})
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    if user.to_dict()["id"] != contract.to_dict()["user_id"] or service.to_dict()["user_id"] != user.to_dict()["id"]:
        raise HTTPException(status_code=403, detail="Unauthorized")
    try:
        contract_data_dict = contract_data.dict()
        storage.update(contract, **contract_data_dict)
        storage.save()
        contract = storage.find_by(Contract, **{"id": contract_id})
        return {"message": "Contract updated successfully", "contract": contract.to_dict()}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# delete contract
@contract_router.delete("/delete/{contract_id}", response_model=dict)
async def delete_contract(contract_id: str, session_id: str = Cookie(None), encrypted_session_id: Optional[str] = None):
    if encrypted_session_id:
        session_id = encrypted_session_id.rstrip('*')

    if session_id is None:
        raise HTTPException(status_code=403, detail="User not logged in")
    
    user = storage.find_by(User, **{"session_id": session_id})
    if user is None:
        raise HTTPException(status_code=403, detail="User session expired")

    if user.to_dict()["is_admin"] != False:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    contract = storage.find_by(Contract, **{"id": contract_id})
    if contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    try:
        storage.delete(contract)
        storage.save()
        return {"message": "Contract deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# get all contracts
@contract_router.get("/", response_model=list)
async def get_all_contracts():
    try:
        contracts = storage.all(Contract)
        contracts_list = [contract.to_dict() for contract in contracts]
        return contracts_list
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# get contract by id
@contract_router.get("/{contract_id}", response_model=dict)
async def get_contract_by_id(contract_id: str):
    contract = storage.find_by(Contract, **{"id": contract_id})
    if contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract.to_dict()

# get contracts by user id
@contract_router.get("/user/{user_id}", response_model=list)
async def get_contracts_by_user_id(user_id: str):
    if user_id is None:
        raise HTTPException(status_code=404, detail="User not found")

    user = storage.find_by(User, **{"id": user_id})

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        contracts = storage.find_all(Contract, **{"user_id": user_id})
        contracts_list = [contract.to_dict() for contract in contracts]
        return contracts_list
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# get contracts by service id
@contract_router.get("/service/{service_id}", response_model=list)
async def get_contracts_by_service_id(service_id: str):
    if service_id is None:
        raise HTTPException(status_code=404, detail="Service not found")
    
    service = storage.find_by(Service, **{"id": service_id})

    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    
    try: 
        contracts = storage.find_all(Contract, **{"service_id": service_id})
        contracts_list = [contract.to_dict() for contract in contracts]
        return contracts_list
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
