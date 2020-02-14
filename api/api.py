from flask import jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from api import marketplace_resources, user_resources
from app import app

api = Api(app)
cors = CORS(app, resources={r'/api/*': {'origins': '*'}})
jwt = JWTManager(app)


@app.route('/')
def index():
    return jsonify({'msg': 'Hello, World!'}), 200


api.add_resource(user_resources.RegularUserRegistration, '/api/register')
api.add_resource(user_resources.RegularUserLogin, '/api/login')
api.add_resource(user_resources.VendorRegistration, '/api/vendor/register')
api.add_resource(user_resources.VendorLogin, '/api/vendor/login')
api.add_resource(user_resources.Profile, '/api/user/profile')
api.add_resource(user_resources.TokenRefresh, '/api/token/refresh')
api.add_resource(user_resources.Shop, '/api/vendor/shop')
api.add_resource(marketplace_resources.Item, '/api/item')
api.add_resource(marketplace_resources.Order, '/api/order')
api.add_resource(marketplace_resources.OrderMap, '/api/order/map')


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user
