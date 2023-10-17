from flask import Blueprint, Flask, jsonify, request
from models.engine.auth import Auth
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from datetime import datetime

auth = Auth()

user_endpoints = Blueprint('user_endpoints', __name__)

# Endpoint to register a new user
@user_endpoints.route('/user/register', methods=['POST'])
def register_user():
    # Get the user data from the request body
    user_data = request.json

    # Validate the user data
    required_fields = {
    "email", "password", "first_name", "last_name",
    "date_of_birth", "gender", "phone_number", "user_image_path",
    "user_video_path", "user_banner_path", "is_admin", "is_active"
    }

    json_keys = set(user_data.keys())

    if required_fields.issubset(json_keys) is False:
        return jsonify({'error': 'Missing fields'}), 400

    user_data['date_of_birth'] = datetime.strptime(user_data['date_of_birth'], '%Y-%m-%d')

    # Register the user using the `auth` object
    try:
        auth.register_user(user_data)
        return jsonify({'message': 'User created successfully', 'email': user_data['email']}), 201
    except ValueError:
        return jsonify({'error': 'User already exists'}), 409
    except InvalidRequestError:
        return jsonify({'error': 'Missing password'}), 400

# Endpoint to login a user
@user_endpoints.route('/user/sessions', methods=['POST'])
def login():
    """
    create a new session for the user,
    store the session ID as a cookie with key
    "session_id" on the response
    and return a JSON payload
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if auth.valid_login(email, password):
        session_id = auth.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response

    return jsonify({"error": "Invalid credentials"})

# Endpoint to logout a user
@user_endpoints.route('/user/sessions', methods=['DELETE'])
def logout():
    """Destroy a user’s session
    """
    session_id = request.cookies.get("session_id")

    user = auth.get_user_from_session_id(session_id)

    if user is None:
        return jsonify({"error": "User not logged in"}), 401

    response = jsonify({"email": None, "message": "logged out"})
    response.set_cookie("session_id", None)

# Endpoint to get the user profile details
@user_endpoints.route("/user/profile", methods=["GET"])
def profile():
    """
    Return the current user’s profile
    """
    session_id = request.cookies.get("session_id")
    user = auth.get_user_from_session_id(session_id)
    if user is None:
        return jsonify({"error": "User not logged in"}), 401
    user_data = user.to_dict()
    del user_data["hashed_password"]
    del user_data["reset_token"]
    del user_data["verification_token"]
    del user_data["session_id"]
    return jsonify(user_data)


# Endpoint to update the user details
@user_endpoints.route('/user/profile', methods=['PUT'])
def update_user_details():
    # Get the session ID from the request
    session_id = request.cookies.get("session_id")
    # Check if the user is logged in
    user = auth.get_user_from_session_id(session_id)
    if user is None:
        return jsonify({"error": "User not logged in"}), 401

    # Get the user data from the request body
    user_data = request.json

    # Update the user details using the `auth` object
    auth.update_user_details(user_data)

    # Return the updated user object
    user = auth.get_user_details()
    user_data = user.to_dict()
    del user_data["hashed_password"]
    del user_data["reset_token"]
    del user_data["verification_token"]
    del user_data["session_id"]

    return jsonify(user_data), 200