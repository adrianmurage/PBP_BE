from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
)
from flask_restful import Resource, reqparse

from models import Users

user_instance = Users()
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', help='This field cannot be blank', required=True)
user_parser.add_argument('password', help='This field cannot be blank', required=True)


class RegularUserRegistration(Resource):
    def post(self):
        data = user_parser.parse_args()

        # if user exists
        current_user = user_instance.find_user_by_username(data['username'])
        if current_user:
            return {'message': 'username {} already exists'.format(data['username'])}

        new_user = {
            'username': data['username'],
            'password': user_instance.generate_hash(data['password']),
            'is_vendor': False
        }
        try:
            user_instance.register_user(new_user)
            return {'message': 'User {} was successfully created'.format(data['username'])}, 200
        except:
            return {'message': 'Something went wrong'}, 500


class RegularUserLogin(Resource):
    def post(self):
        data = user_parser.parse_args()
        current_user = user_instance.find_user_by_username(data['username'])

        # if current_user['_id'] == ObjectId(str(current_user['_id'])):
        #     print(True)

        # if user does not exist
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        if user_instance.verify_hash(data['password'], current_user['password']):
            user = {
                'username': current_user['username'],
                '_id': str(current_user['_id'])
            }
            access_token = create_access_token(user)
            refresh_token = create_refresh_token(user)
            return {
                       'message': 'Logged in as {}'.format(current_user['username']),
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200
        else:
            return {'message': 'Wrong credentials'}, 401


class VendorRegistration(Resource):
    def post(self):
        data = user_parser.parse_args()

        # if user exists
        current_user = user_instance.find_user_by_username(data['username'])
        if current_user:
            return {'message': 'username {} already exists'.format(data['username'])}

        new_user = {
            'username': data['username'],
            'password': user_instance.generate_hash(data['password']),
            'is_vendor': True
        }
        try:
            user_instance.register_user(new_user)
            return {'message': 'Vendor {} was successfully created'.format(data['username'])}, 200
        except:
            return {'message': 'Something went wrong'}, 500


class VendorLogin(Resource):
    def post(self):
        data = user_parser.parse_args()
        current_user = user_instance.find_user_by_username(data['username'])

        # if vendor does not exist
        if not current_user:
            return {'message': 'Vendor {} doesn\'t exist'.format(data['username'])}

        if user_instance.verify_hash(data['password'], current_user['password']):
            user = {
                'username': current_user['username'],
                '_id': str(current_user['_id'])
            }
            access_token = create_access_token(user)
            refresh_token = create_refresh_token(user)
            return {
                       'message': 'Logged in as {}'.format(current_user['username']),
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200
        else:
            return {'message': 'Wrong credentials'}, 401


class LogoutAccess(Resource):
    def post(self):
        return {'message': 'regular user logout'}


class LogoutRefresh(Resource):
    def post(self):
        return {'message': 'regular user logout'}


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        user = get_jwt_identity()
        access_token = create_access_token(identity=user)
        return {'access_token': access_token}, 200


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return get_jwt_identity()
