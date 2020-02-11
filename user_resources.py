import datetime

from bson.objectid import ObjectId
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


class Profile(Resource):
    @jwt_required
    def get(self):
        regular_user_id = get_jwt_identity()['regular_user_id']
        try:
            user = user_instance.find_user_by_id(ObjectId(regular_user_id))
            user_details = {
                'username': user['username']
            }
            return user_details
        except:
            return {'msg': 'Something went wrong'}, 500


class RegularUserRegistration(Resource):
    def post(self):
        data = user_parser.parse_args()

        # if username is ''
        if data['username'] == '' or None:
            return {'msg': 'username cannot be blank'}, 401
        # if user exists
        current_user = user_instance.find_user_by_username(data['username'])
        if current_user:
            return {'msg': 'username {} already exists'.format(data['username'])}, 401

        new_regular_user = {
            'username': data['username'],
            'password': user_instance.generate_hash(data['password']),
            'is_vendor': False,
            'created_at': datetime.datetime.now()
        }
        try:
            user_instance.save(new_regular_user)
            return {'msg': 'User {} was successfully created'.format(data['username'])}, 200
        except:
            return {'msg': 'Something went wrong'}, 500


class RegularUserLogin(Resource):
    def post(self):
        data = user_parser.parse_args()
        current_user = user_instance.find_user_by_username(data['username'])

        # if user does not exist
        if not current_user:
            return {'msg': 'User {} doesn\'t exist'.format(data['username'])}, 401

        if user_instance.verify_hash(data['password'], current_user['password']):
            user = {
                'username': current_user['username'],
                'regular_user_id': str(current_user['_id'])
            }
            access_token = create_access_token(user)
            refresh_token = create_refresh_token(user)
            return {
                       'msg': 'Logged in as {}'.format(current_user['username']),
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200
        else:
            return {'msg': 'Wrong credentials'}, 401


class VendorRegistration(Resource):
    def post(self):
        data = user_parser.parse_args()

        # if user exists
        current_user = user_instance.find_user_by_username(data['username'])
        if current_user:
            return {'msg': 'username {} already exists'.format(data['username'])}, 401

        new_vendor = {
            'username': data['username'],
            'password': user_instance.generate_hash(data['password']),
            'is_vendor': True,
            'created_at': datetime.datetime.now()
        }
        try:
            user_instance.save(new_vendor)
            return {'msg': 'Vendor {} was successfully created'.format(data['username'])}, 200
        except:
            return {'msg': 'Something went wrong'}, 500


class VendorLogin(Resource):
    def post(self):
        data = user_parser.parse_args()
        current_user = user_instance.find_user_by_username(data['username'])

        # if vendor does not exist
        if not current_user:
            return {'msg': 'Vendor {} doesn\'t exist'.format(data['username'])}, 401

        if user_instance.verify_hash(data['password'], current_user['password']):
            user = {
                'username': current_user['username'],
                'vendor_id': str(current_user['_id'])
            }
            access_token = create_access_token(user)
            refresh_token = create_refresh_token(user)
            return {
                       'msg': 'Logged in as {}'.format(current_user['username']),
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200
        else:
            return {'msg': 'Wrong credentials'}, 401


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        user = get_jwt_identity()
        access_token = create_access_token(identity=user)
        return {'access_token': access_token}, 200
