from flask import Flask
from api.user_endpoints import user_endpoints
app = Flask(__name__)

# Register the user endpoints blueprint
app.register_blueprint(user_endpoints)

if __name__ == '__main__':
    app.run(debug=True)