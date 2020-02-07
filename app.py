from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask import jsonify

import resources

app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})


cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
jwt = JWTManager(app)

app.config['JWT_SECRET_KEY'] = 'JrR&A7z3#jdxpASvAE18J$%m0tb9TK@P'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

api.add_resource(resources.RegularUserRegistration, '/api/register')
api.add_resource(resources.RegularUserLogin, '/api/login')
api.add_resource(resources.RegularUserLogoutAccess, '/api/logout/access')
api.add_resource(resources.RegularUserLogoutRefresh, '/api/logout/refresh')
api.add_resource(resources.RegularUserTokenRefresh, '/api/token/refresh')
api.add_resource(resources.SecretResource, '/api/secret')

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=500 0)
