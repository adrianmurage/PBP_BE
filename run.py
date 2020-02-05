from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

from PBP_BE import views, models, resources

api.add_resource(resources.RegularUserRegistration, '/registration')
api.add_resource(resources.RegularUserLogin, '/login')
api.add_resource(resources.RegularUserLogoutAccess, '/logout/access')
api.add_resource(resources.RegularUserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.RegularUserTokenRefresh, '/token/refresh')
api.add_resource(resources.SecretResource, '/secret')
