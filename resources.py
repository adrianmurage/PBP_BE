from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity
)
from flask_restful import Resource, reqparse

from PBP_BE.models import Users

regular_user = Users("REGULAR")
regular_user_parser = reqparse.RequestParser()
regular_user_parser.add_argument('username', help='This field cannot be blank', required=True)
regular_user_parser.add_argument('password', help='This field cannot be blank', required=True)


class RegularUserRegistration(Resource):
    def post(self):
        data = regular_user_parser.parse_args()

        # if user exists
        current_user = regular_user.find_user_by_username(data["username"])
        if current_user:
            return {'message': 'User {} already exists'.format(data['username'])}

        new_user = {
            "username": data["username"],
            "password": regular_user.generate_hash(data["password"])
        }
        try:
            regular_user.register_user(new_user)
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                       'message': 'User {} was successfully created'.format(data["username"]),
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200
        except:
            return {'message': 'Something went wrong'}, 500


class RegularUserLogin(Resource):
    def post(self):
        data = regular_user_parser.parse_args()
        current_user = regular_user.find_user_by_username(data["username"])
        print(current_user)

        # if user does not exist
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        if regular_user.verify_hash(data['password'], current_user['password']):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                       'message': 'Logged in as {}'.format(current_user['username']),
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200
        else:
            return {'message': 'Wrong credentials'}, 401


class RegularUserLogoutAccess(Resource):
    def post(self):
        return {'message': 'regular user logout'}


class RegularUserLogoutRefresh(Resource):
    def post(self):
        return {'message': 'regular user logout'}


class RegularUserTokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}, 200


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {'value': True}
