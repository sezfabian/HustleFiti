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
    """
    Registers a new user with the provided user data.

    Parameters:
        - user_data: An instance of the UserCreate model representing the data of the user to be registered.

    Returns:
        - A dictionary with the following keys:
            - "message": A string indicating the success message.
            - "email": The email address of the registered user.

    Raises:
        - HTTPException with status code 409 if a value error occurs during registration.
        - HTTPException with status code 400 if any other exception occurs during registration.
    """
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
    """
    Endpoint to handle user login sessions.

    Parameters:
        - session: The user session object containing the email and password.
        - session_id: The session ID stored in a cookie.

    Returns:
        - If the login is successful, a JSON response with the user's email, a success message,
          and an encrypted session ID in the headers.
        - If the login fails, an HTTPException with a status code of 401 and a detail message.

    Raises:
        - HTTPException: If the login credentials are invalid.
    """
    email = session.email
    password = session.password
    if auth.valid_login(email, password):
        session_id = auth.create_session(email)
        response = {"email": email, "message": "logged in", "encrypted_session_id": session_id + "********"}
        return JSONResponse(content=response, headers={"Set-Cookie": f"session_id={session_id}; Path=/;"})
    raise HTTPException(status_code=401, detail="Invalid credentials")

@user_router.delete("/sessions", response_model=dict)
async def logout(session_id: str = Cookie(None), encrypted_session_id: Optional[str] = None):
    """
    Delete a session and log out the user.

    Parameters:
        session_id (str): The session ID of the user. It is obtained from the session cookie.
        encrypted_session_id (Optional[str]): An optional encrypted session ID. If provided, it will be decrypted and used as the session ID.

    Returns:
        dict: A dictionary containing the email and message indicating that the user has been logged out.

    Raises:
        HTTPException: If the user is not logged in.

    """
    if encrypted_session_id:
        session_id = encrypted_session_id.rstrip('*')
    user = auth.get_user_from_session_id(session_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not logged in")
    response = {"email": None, "message": "logged out"}
    return JSONResponse(content=response, headers={"Set-Cookie": "session_id=; Path=/; Max-Age=0;"})

@user_router.get("/profile", response_model=dict)
async def profile(session_id: str = Cookie(None), encrypted_session_id: Optional[str] = None):
    """
    Retrieves the profile information of a user.

    Parameters:
        session_id (str): The session ID of the user. Retrieved from the cookie.
        encrypted_session_id (Optional[str]): An optional encrypted session ID.

    Returns:
        dict: A dictionary containing the user's profile information, excluding sensitive data.
    """
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
async def update_user_details(user_data: Dict, session_id: str = Cookie(None), encrypted_session_id: Optional[str] = None):
    """
    Update user details.

    Args:
        user_data (Dict): A dictionary containing the user's data.
        session_id (str, optional): The session ID of the user. Defaults to None.
        encrypted_session_id (str, optional): The encrypted session ID of the user. Defaults to None.

    Returns:
        dict: A dictionary containing the updated user data.

    Raises:
        HTTPException: If the user is not logged in.
        HTTPException: If there is an error updating the user details.
    """
    if encrypted_session_id:
        session_id = encrypted_session_id.rstrip('*')

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
    """
    Verify a user's account using the provided verification data.

    Args:
        verification_data (UserVerification): The verification data containing the email and token.

    Returns:
        dict: A dictionary with a message indicating whether the user was verified successfully.

    Raises:
        HTTPException: If the verification code is invalid.
    """
    try:
        auth.verify_account(verification_data.email, verification_data.token)
        return {"message": "User verified successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Verification Code invalid")

#Delete user account
@user_router.delete("/delete", response_model=dict)
async def delete_user(session_id: str = Cookie(None), encrypted_session_id: Optional[str] = None):
    """
    Deletes a user.

    Parameters:
        session_id (str): The session ID of the user. It is obtained from the cookie.
        encrypted_session_id (Optional[str]): An optional encrypted session ID. If provided, the function will use this instead of the session ID obtained from the cookie.

    Returns:
        dict: A dictionary containing the message "User deleted successfully" if the user was deleted successfully.

    Raises:
        HTTPException: If the user is not logged in or if the user is not found.
    """
    if encrypted_session_id:
        session_id = encrypted_session_id.rstrip('*')
    user = auth.get_user_from_session_id(session_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not logged in")
    if auth.delete_user(user):
        return {"message": "User deleted successfully"}

    raise HTTPException(status_code=404, detail="User not found")
