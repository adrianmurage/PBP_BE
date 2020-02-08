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
item_instance = Marketplace("ITEMS")
item_parser = reqparse.RequestParser()
item_parser.add_argument('item_name', help="This field cannot be blank", required=True)
item_parser.add_argument('item_quantity', help="this field cannot be empty", required=True)


class Shop(Resource):
    @jwt_required
    def post(self):
        data = shop_parser.parse_args()
        vendor_id = get_jwt_identity()['_id']
        shop_details0 = shop_instance.find_shop_by_vendor_id(ObjectId(vendor_id))
        shop_details1 = shop_instance.find_shop_by_shop_name(
            shop_details0['shop_name']
        )
        # if shop exists
        if shop_details0:
            return {'message': 'shop {} already exists'.format(data['shop_name'])}
        if shop_details1:
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
            shop_instance.save(new_shop)
            return {'message': 'Shop {} was successfully created'.format(data['shop_name'])}, 200
        except:
            return {'message': 'Something went wrong'}, 500


class Item(Resource):
    @jwt_required
    def post(self):
        data = item_parser.parse_args()
        print(data)
        vendor_id = get_jwt_identity()['_id']
        shop_details = shop_instance.find_shop_by_vendor_id(ObjectId(vendor_id))
        item_details = item_instance.find_item_by_name(data['item_name'])
        # if shop does not exist
        if not shop_details:
            return {'message': 'The current vendor\'s shop does not exists'}, 404
        # if item exists increment quantity
        if item_details:
            item_instance.increment_item_quantity(
                data['item_name'],
                ObjectId(vendor_id),
                int(data['item_quantity'])
            )
            return {'message': 'Incremented item {0} by {1}'.format(
                data['item_name'],
                data['item_quantity']
            )}

        new_item = {
            'item_name': data['item_name'],
            'item_quantity': int(data['item_quantity']),
            'vendor_id': ObjectId(vendor_id),
            'shop_id': shop_details['_id']
        }
        try:
            item_instance.save(new_item)
            return {'message': 'item {} was successfully added'.format(data['item_name'])}
        except:
            return {'message': 'Something went wrong'}, 500
