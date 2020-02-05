from flask_restful import Resource, reqparse

regular_user_parser = reqparse.RequestParser()
regular_user_parser.add_argument('username', help='This field cannot be blank', required=True)
regular_user_parser.add_argument('password', help='This field cannot be blank', required=True)


class RegularUserRegistration(Resource):
    def post(self):
        data = regular_user_parser.parse_args()
        return data


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