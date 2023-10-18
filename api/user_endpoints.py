from flask import Blueprint
from flask_restx import Api, Resource, fields
from models.engine.auth import Auth
from datetime import datetime

auth = Auth()

user_blueprint = Blueprint('user_api', __name__)
api = Api(user_blueprint)

user_model = api.model('User', {
    "email": fields.String(required=True),
    "password": fields.String(required=True),
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True),
    "date_of_birth": fields.Date(required=True),
    "gender": fields.String(required=True),
    "phone_number": fields.String(required=True),
    "user_image_path": fields.String(required=True),
    "user_video_path": fields.String(required=True),
    "user_banner_path": fields.String(required=True),
    "is_admin": fields.Boolean(required=True),
    "is_active": fields.Boolean(required=True),
})


class UserRegistration(Resource):
    @api.expect(user_model, validate=True)
    def post(self):
        user_data = api.payload

        # Validate the user data
        required_fields = set(user_model.keys())
        provided_fields = set(user_data.keys())

        if not required_fields.issubset(provided_fields):
            return {'error': 'Missing fields'}, 400

        user_data['date_of_birth'] = datetime.strptime(user_data['date_of_birth'], '%Y-%m-%d')

        try:
            auth.register_user(user_data)
            return {'message': 'User created successfully', 'email': user_data['email']}, 201
        except ValueError:
            return {'error': 'User already exists'}, 409
        except InvalidRequestError:
            return {'error': 'Missing password'}, 400


class UserSession(Resource):
    def post(self):
        email = api.payload.get("email")
        password = api.payload.get("password")

        if auth.valid_login(email, password):
            session_id = auth.create_session(email)
            response = {'email': email, 'message': 'logged in'}
            return response, 200

        return {'error': 'Invalid credentials'}, 401


class UserProfile(Resource):
    def get(self):
        session_id = api.payload.get("session_id")
        user = auth.get_user_from_session_id(session_id)

        if user is None:
            return {"error": "User not logged in"}, 401

        user_data = user.to_dict()
        del user_data["hashed_password"]
        del user_data["reset_token"]
        del user_data["verification_token"]
        del user_data["session_id"]
        return user_data

    @api.expect(user_model, validate=True)
    def put(self):
        session_id = api.payload.get("session_id")
        user = auth.get_user_from_session_id(session_id)

        if user is None:
            return {"error": "User not logged in"}, 401

        user_data = api.payload
        auth.update_user_details(user_data)

        user = auth.get_user_details()
        user_data = user.to_dict()
        del user_data["hashed_password"]
        del user_data["reset_token"]
        del user_data["verification_token"]
        del user_data["session_id"]
        return user_data, 200
