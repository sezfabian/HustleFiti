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

contract_model = api.model('contract_model', {
    "id": fields.String,
    "created_at": fields.String,
    "updated_at": fields.String,
    "user_id": fields.String,
    "service_id": fields.String,
    "location": fields.String,
    "duration": fields.String,
    "price_package_id": fields.String,
    "total_amount": fields.Float,
    "contract_start_date": fields.String,
    "contract_end_date": fields.String,
    "contract_status": fields.String,
    "paid_amount": fields.String
})

contract_model_input = api.model('contract_model_imput', {
    "user_id": fields.String,
    "service_id": fields.String,
    "location": fields.String,
    "duration": fields.String,
    "price_package_id": fields.String,
    "total_amount": fields.Float,
    "contract_start_date": fields.String,
    "contract_end_date": fields.String,
    "contract_status": fields.String,
    "paid_amount": fields.String
})


service_reviews_model = api.model('service_reviews', {
    "id": fields.String(format='uuid'),
    "created_at": fields.String,
    "updated_at": fields.String,
    "user_id": fields.String,
    "contract_id": fields.String,
    "service_id": fields.String,
    "rating": fields.String,
    "comment": fields.String
})

service_reviews_model_input = api.model('service_reviews_input', {
    "user_id": fields.String,
    "contract_id": fields.String,
    "service_id": fields.String,
    "rating": fields.String,
    "comment": fields.String
})


client_reviews_model = api.model('client_review', {
    "id": fields.String,
    "created_at": fields.String,
    "updated_at": fields.String,
    "contract_id": fields.String,
    "user_id": fields.String,
    "rating": fields.Float,
    "comment": fields.String
})

client_reviews_model_input = api.model('client_review_input', {
    "contract_id": fields.String,
    "user_id": fields.String,
    "rating": fields.Float,
    "comment": fields.String
})
