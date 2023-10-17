#!/usr/bin/env python3
"""authentication module
"""
import bcrypt
import uuid
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from models import storage
from models import mail
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
    
    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Find a user by session_id
        returns the corresponding User or None.
        """
        if session_id is None:
            return None

        user = self._db.find_by(User, **{"session_id": session_id})
        if user:
            return user
        
        return None

    def destroy_session(self, user_id: str) -> None:
        """
        Destroy a user’s session.
        """
        user = self._db.find_by(User, **{"id": user_id})
        if user:
            self._db.update(user, **{"session_id": None})

        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Find the user corresponding to the email.
        If the user does not exist,
        raise a ValueError exception.
        If it exists, generate a UUID and
        update the user’s reset_token database field.
        Finally, Return the token.
        """
        user = self._db.find_by(User, **{"email": email})
        if user:
            reset_token = _generate_uuid()
            self._db.update(user, **{"reset_token": reset_token})
            mail.send({
                "email": user.email,
                "name": user.name,
                "reset_token": reset_token
            })

            return reset_token

        return None

    def update_password(self, reset_token: str, password: str) -> None:
        """
        takes reset_token string argument
        and a password string argument.
        Uses the reset_token to find the corresponding user.
        If it does not exist, raise a ValueError exception.
        Otherwise, hash the password and update the user’s
        hashed_password field with the new hashed password
        and the reset_token field to None.
        """
        user = self._db.find_by(User, **{"reset_token": reset_token})
        if user:
            hashed_password = _hash_password(password)
            self._db.update(user, **{"hashed_password": hashed_password, "reset_token": None})
            return "Password updated"

        return None

    def verify_account(self, email: str, token: str) -> bool:
        """
        Find the user corresponding to the email.
        If it does not exist, raise a ValueError exception.
        Otherwise, check the password with bcrypt.checkpw.
        If it matches, return True.
        Otherwise, return False.
        """
        user = self._db.find_by(User, **{"email": email})
        if user:
            if user.is_verified:
                return 
            return False