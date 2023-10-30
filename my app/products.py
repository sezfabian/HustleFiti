from flask import Blueprint, jsonify, request

products_bp = Blueprint('products', __name__, url_prefix='/products')   # Blueprint for products

products = []

@products_bp.route('/', methods=['GET', 'POST'])
def handle_products():
    if request.method == 'GET':
        return jsonify(products)
    else:
        request_body = request.get_json()
        required_fields = ['user_id', 'category', 'product_description', 'price', 'cost' 'product_image_paths']
        for field in required_fields:
            if not request_body.get(field):
                return jsonify(f'Missing field: {field}'), 400
        product = {
            'user_id': request_body['user_id'],
            'category': request_body['category'],
            'product_description': request_body['product_description'],
            'price': request_body['price'],
            'cost': request_body['cost'],
            'product_image_paths': request_body['product_image_paths']
        }
        products.append(product)
        return jsonify(product), 201    