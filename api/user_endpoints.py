from os import getenv
from fastapi import APIRouter, HTTPException, Depends, Cookie
from fastapi.responses import JSONResponse
from models.engine.auth import Auth
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Dict

auth = Auth()

user_router = APIRouter()

class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    username: str
    date_of_birth: str 
    gender: str
    phone_number: str = None
    user_image_path: str = None
    user_video_path: str = None
    user_banner_path: str = None

class UserSession(BaseModel):
    email: str
    password: str

class UserVerification(BaseModel):
    email: str
    token: str

@user_router.post("/register", response_model=dict)
async def register_user(user_data: UserCreate):
    try:
        user_data_dict = user_data.dict()
        user_data_dict['date_of_birth'] = user_data.date_of_birth
        auth.register_user(user_data_dict)
        return {"message": "User created successfully", "email": user_data.email}
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_router.post("/sessions", response_model=dict)
async def login(session: UserSession, session_id: str = Cookie(None)):
    email = session.email
    password = session.password
    if auth.valid_login(email, password):
        session_id = auth.create_session(email)
        response = {"email": email, "message": "logged in", "encrypted_session_id": session_id + "********"}
        return JSONResponse(content=response, headers={"Set-Cookie": f"session_id={session_id}; Path=/;"})
    raise HTTPException(status_code=401, detail="Invalid credentials")

@user_router.delete("/sessions", response_model=dict)
async def logout(session_id: str = Cookie(None)):
    user = auth.get_user_from_session_id(session_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not logged in")
    response = {"email": None, "message": "logged out"}
    return JSONResponse(content=response, headers={"Set-Cookie": "session_id=; Path=/; Max-Age=0;"})

@user_router.get("/profile", response_model=dict)
async def profile(session_id: str = Cookie(None), encrypted_session_id: Optional[str] = None):
    if encrypted_session_id:
        session_id = encrypted_session_id.rstrip('*')
    user = auth.get_user_from_session_id(session_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not logged in")
    user_data = user.to_dict()
    del user_data["hashed_password"]
    del user_data["reset_token"]
    del user_data["verification_token"]
    del user_data["session_id"]
    del user_data["__class__"]
    return user_data

@user_router.put("/profile", response_model=dict)
async def update_user_details(user_data: Dict, session_id: str = Cookie(None)):
    user = auth.get_user_from_session_id(session_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not logged in")
    try:
        user_data["session_id"] = session_id
        updated_user = auth.update_user_details(user_data, user)
        user_data = updated_user.to_dict()
        del user_data["hashed_password"]
        del user_data["reset_token"]
        del user_data["verification_token"]
        del user_data["session_id"]
        del user_data["__class__"]
        return user_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_router.post("/verify", response_model=dict)
async def verify(verification_data: UserVerification):
    try:
        auth.verify_account(verification_data.email, verification_data.token)
        return {"message": "User verified successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Verification Code invalid")

#Delete user account
@user_router.delete("/delete", response_model=dict)
async def delete_user(session_id: str = Cookie(None)):
    user = auth.get_user_from_session_id(session_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not logged in")
    if auth.delete_user(user):
        return {"message": "User deleted successfully"}

    raise HTTPException(status_code=404, detail="User not found")
