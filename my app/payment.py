from flask import Flask,request, jsonify

app = Flask(__name__)

payments_db = []

@app.route('/initialize_payments', methods=['POST'])
def initialize_payments():
    request_body = request.get_json()

    new_payment = {
        'user_id': request_body['user_id'],
        'payment_id': request_body['payment_id'],
        'amount': request_body['amount'],
        'payment_method': request_body['payment_method'],
        'payment_date': request_body['payment_date'],
        'payment_status': request_body['payment_status']
    }

    payments_db.append(new_payment)
    return jsonify(new_payment), 201

if __name__ == '__main__':
    app.run(debug=True)

