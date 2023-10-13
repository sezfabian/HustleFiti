from flask import Flask, request, jsonify

app = Flask(__name__)

users_db = []

@app.route('/users', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'GET':
        return jsonify(users_db)

    elif request.method == 'POST':
        user_data = request.get_json()
        # Validate the user_data here.

        new_user = {
            'id': len(users_db) + 1,
            'email': user_data['email'],
            'hashed_password': user_data['hashed_password'],
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'date_of_birth': user_data['date_of_birth'],
            'created_at': user_data['created_at'],
            'updated_at': user_data['updated_at'],
            'user_image_path': user_data['user_image_path'],
            'user_video_path': user_data['user_video_path'],
            'user_wallpaper_path': user_data['user_wallpaper_path']
        }

        users_db.append(new_user)
        return jsonify(new_user), 201

@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_user(user_id):
    if request.method == 'GET':
        user = next((user for user in users_db if user['id'] == user_id), None)
        if user:
            return jsonify(user), 200
        return 'User not found', 404

    elif request.method == 'PUT':
        user_data = request.get_json()
        # Update the user with the new data.
        # Validate and update the fields as needed.
        return jsonify(user_data), 200

    elif request.method == 'DELETE':
        user = next((user for user in users_db if user['id'] == user_id), None)
        if user:
            users_db.remove(user)
            return 'User deleted', 200
        return 'User not found', 404

if __name__ == '__main__':
    app.run(debug=True)
