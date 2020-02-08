from bson.objectid import ObjectId
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from flask_restful import Resource, reqparse

from models import Marketplace

shop_instance = Marketplace("SHOPS")
shop_parser = reqparse.RequestParser()
shop_parser.add_argument('shop_name', help='This field cannot be blank', required=True)
shop_parser.add_argument('shop_lat', help='This field cannot be blank', required=True)
shop_parser.add_argument('shop_lng', help='This field cannot be blank', required=True)


class Shop(Resource):
    @jwt_required
    def post(self):
        data = shop_parser.parse_args()
        vendor_id = get_jwt_identity()['_id']
        shop_details = shop_instance.find_shop_by_vendor_id(ObjectId(vendor_id))

        # if shop exists
        if shop_details:
            return {'message': 'shop {} already exists'.format(data['shop_name'])}

        new_shop = {
            'shop_name': data['shop_name'],
            'shop_location': {
                'lat': int(data['shop_lat']),
                'lng': int(data['shop_lng'])
            },
            'vendor_id': ObjectId(vendor_id)
        }
        try:
            shop_instance.save_shop(new_shop)
            return {'message': 'Shop {} was successfully created'.format(data['shop_name'])}, 200
        except:
            return {'message': 'Something went wrong'}, 500
