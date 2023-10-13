from flask import Blueprint, jsonify, request

sales_bp = Blueprint('sales', __name__, url_prefix='/sales')   # Blueprint for sales

sales = []

@sales_bp.route('/', methods=['GET', 'POST'])
def handle_sales():
    if request.method == 'GET':
        return jsonify(sales)
    else:
        request_body = request.get_json()
        required_fields = ['user_id', 'product_id', 'quantity', 'total_price', 'total_cost', 'profit']
        for field in required_fields:
            if not request_body.get(field):
                return jsonify(f'Missing field: {field}'), 400
        sale = {
            'user_id': request_body['user_id'],
            'product_id': request_body['product_id'],
            'quantity': request_body['quantity'],
            'total_price': request_body['total_price'],
            'total_cost': request_body['total_cost'],
            'profit': request_body['profit']
        }
        sales.append(sale)
        return jsonify(sale), 201