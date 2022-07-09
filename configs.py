import datetime
import os

from app import app

# flask app
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=10)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=10)

# MongoDB
MONGO_USER = os.environ.get('MONGO_USER')
MONGO_PSWD = os.environ.get('MONGO_PSWD')


