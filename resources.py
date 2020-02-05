from flask_restful import Resource, reqparse

from PBP_BE.models import Users

regular_user_parser = reqparse.RequestParser()
regular_user_parser.add_argument('username', help='This field cannot be blank', required=True)
regular_user_parser.add_argument('password', help='This field cannot be blank', required=True)


class RegularUserRegistration(Resource):
    def post(self):
        data = regular_user_parser.parse_args()
        regular_user = Users("REGULAR")

        # if user exists
        if regular_user.find_user_by_username(data["username"]):
            return {'message': 'User {} already exists'.format(data['username'])}

        new_user = {
            "username": data["username"],
            "password": data["password"]
        }
        try:
            regular_user.register_user(new_user)
            return {
                'message': 'User {} was created'.format(data["username"])
            }
        except:
            return {'message': 'Something went wrong'}, 500


class RegularUserLogin(Resource):
    def post(self):
        data = regular_user_parser.parse_args()
        return data


class RegularUserLogoutAccess(Resource):
    def post(self):
        return {'message': 'regular user logout'}


class RegularUserLogoutRefresh(Resource):
    def post(self):
        return {'message': 'regular user logout'}


class RegularUserTokenRefresh(Resource):
    def post(self):
        return {'message': 'regular user token refresh'}


class SecretResource(Resource):
    def get(self):
        return {'value': True}
