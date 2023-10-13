from flask_restx import fields
from .extensions import api

services_model = api.model('services', {
    "id": fields.String,
    "created_at": fields.String,
    "updated_at": fields.String,
    "user_id": fields.String,
    "name": fields.String,
    "description": fields.String,
    "service_category_id": fields.String,
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



service_category_model = api.model('service_category', {
    "id": fields.String,
    "created_at": fields.String,
    "updated_at": fields.String,
    "name": fields.String,
    "sub_catergories": fields.String
})

service_category_model_input = api.model('service_category_input', {
    "name": fields.String,
    "sub_categories": fields.String
})

price_packages_model = api.model('price_packages', {
    "id": fields.String,
    "created_at": fields.String,
    "updated_at": fields.String,
    "service_id": fields.String,
    "name": fields.String,
    "description": fields.String,
    "price": fields.Float(attribute='price'),
    "duration": fields.String
})


price_packages_model_input = api.model('price_packages_input', {
    "name": fields.String,
    "service_id": fields.String,
    "description": fields.String,
    "price": fields.Float(attribute='price'),
    "duration": fields.String
})


