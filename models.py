import pymongo
from passlib.hash import pbkdf2_sha256 as sha256


class Mongo:
    """
    database object
    this class is overridden by sub-classes below
    """

    def __init__(self, database='USERS'):
        """

        :param database: string
                        the name of the database to be used
        """
        # TODO move config variables to env
        mongo_uri = 'mongodb+srv://{user}:{pswd}@pbp-dkuv8.azure.mongodb.net/test?retryWrites=true&w=majority'.format(
            user='adrianmurage',
            pswd='y6q85ymUp8PgGhZ2'
        )
        self.mongo = pymongo.MongoClient(mongo_uri)[database]


class Users(Mongo):
    """
    class for user related db interactions
    """

    def __init__(self):
        super(Users, self).__init__('USERS')
        self.db = self.mongo['ALL_USERS']

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hashed_password):
        return sha256.verify(password, hashed_password)

    def save(self, user_details):
        """
        adds new users to the db
        :param user_details: dictionary
                            a dict with the users details
        :return:
        """
        self.db.insert_one(user_details)

    def find_user_by_username(self, username):
        """
        checks if a user with the username exists
        :param username: string
        :return:
        """
        user = self.db.find_one(
            {'username': username}
        )
        return user


class Marketplace(Mongo):
    """
    Class for market place collection
    """

    def __init__(self, collection):
        super(Marketplace, self).__init__('MARKETPLACE')
        self.db = self.mongo[collection]

    def save(self, payload):
        self.db.insert_one(payload)

    def find_shop_by_vendor_id(self, vendor_id):
        shop_details = self.db.find_one(
            {'vendor_id': vendor_id}
        )
        return shop_details

    def find_shop_by_shop_name(self, shop_name):
        shop_details = self.db.find_one(
            {'shop_name': shop_name}
        )
        return shop_details

    def find_item_by_name(self, item_name):
        item_details = self.db.find_one(
            {'item_name': item_name}
        )
        return item_details

    def increment_item_quantity(self, item_name, vendor_id, item_quantity: int):
        self.db.update(
            {
                'item_name': item_name,
                'vendor_id': vendor_id
            },
            {'$inc': {'item_quantity': item_quantity}}
        )

    def find_items(self):
        items = self.db.find({})
        return items
