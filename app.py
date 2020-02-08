import datetime

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

import marketplace_resources
import user_resources

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r'/api/*': {'origins': '*'}})
jwt = JWTManager(app)

app.config['JWT_SECRET_KEY'] = 'JrR&A7z3#jdxpASvAE18J$%m0tb9TK@P'
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=10)


@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})


api.add_resource(user_resources.RegularUserRegistration, '/api/register')
api.add_resource(user_resources.RegularUserLogin, '/api/login')
api.add_resource(user_resources.VendorRegistration, '/api/vendor/register')
api.add_resource(user_resources.VendorLogin, '/api/vendor/login')
api.add_resource(user_resources.LogoutAccess, '/api/logout/access')
api.add_resource(user_resources.LogoutRefresh, '/api/logout/refresh')
api.add_resource(user_resources.TokenRefresh, '/api/token/refresh')
api.add_resource(user_resources.SecretResource, '/api/secret')
api.add_resource(marketplace_resources.Shop, '/api/vendor/shop')
api.add_resource(marketplace_resources.Item, '/api/vendor/item')


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
