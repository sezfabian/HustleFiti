#!/usr/bin/env python3
"""authentication module
"""
import bcrypt
import uuid
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from models import storage
from models.user import User


def _hash_password(password: str) -> bytes:
    """Hashes password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """return a string representation of a new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = storage

    def register_user(self, user_data: dict) -> User:
        """Register new user
        """

        # Check if email already exists
        unique_data = {
            "email": user_data["email"],
        }
        user = self._db.find_by(User, **unique_data)   
        if user:
            raise ValueError("User {} already exists".format(user_data["email"]))
        
        # create local user data with hashed password
        user_data_local = user_data.copy()

        # Check if password is valid
        if 'password' in user_data_local:
            password = user_data["password"]
            del user_data_local["password"]
            user_data_local["hashed_password"] = _hash_password(password)
        else:
            raise InvalidRequestError("Missing password")
        
        # Create new user    
        user_data_local["hashed_password"] = _hash_password(password)
        user = User(**user_data_local)
        self._db.new(user)
        self._db.save()
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Try locating the user by email.
        If it exists, check the password with bcrypt.checkpw.
        If it matches return True.
        In any other case, return False.
        """
        try:
            user = self._db.find_by(User, **{"email": email})
            stored_password = user.hashed_password.encode('utf-8')  # Ensure stored password is in bytes
            entered_password = password.encode('utf-8')  # Encode entered password to bytes
            if bcrypt.checkpw(entered_password, stored_password):
                return True
        except (NoResultFound, InvalidRequestError):
            return False

        return False
    
    def create_session(self, email: str) -> str:
        """
        Try to find the user corresponding to the email,
        generate a new UUID for the session
        and store it in the database as the user’s session_id,
        then return the session ID.
        """
        
        user = self._db.find_by(User, **{"email": email})
        if user:
            session_id = _generate_uuid()
            self._db.update(user, **{"session_id": session_id})
            return session_id
        return None