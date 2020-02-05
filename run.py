from flask import Flask
from flask_cors import CORS
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

from PBP_BE import resources

api.add_resource(resources.RegularUserRegistration, '/api/registration')
api.add_resource(resources.RegularUserLogin, '/api/login')
api.add_resource(resources.RegularUserLogoutAccess, '/api/logout/access')
api.add_resource(resources.RegularUserLogoutRefresh, '/api/logout/refresh')
api.add_resource(resources.RegularUserTokenRefresh, '/api/token/refresh')
api.add_resource(resources.SecretResource, '/api/secret')
