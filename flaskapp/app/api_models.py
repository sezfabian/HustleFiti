from flask_restx import fields
from .extensions import api

services_model = api.model('services', {
    "id":fields.String,
    "created_at": fields.String,
    "updated_at": fields.String,
    "user_id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "service_category_id": fields.Integer,
    "image_paths": fields.String,
    "video_paths": fields.String,
    "banner_paths": fields.String,
    "is_verified": fields.Integer
})

service_model_input = api.model('service_input', {
    "name": fields.String,
    "user_id": fields.String,
    "service_category_id": fields.String,
    "description": fields.String,
    "image_paths": fields.String,
    "video_paths": fields.String,
    "banner_paths": fields.String,
    "is_verified": fields.Integer
})
