from flask_restx import fields
from .extensions import api

services_model = api_model('services', {
    "id" = fields.Integer,
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
