import datetime

from bson.objectid import ObjectId
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from flask_restful import Resource, reqparse

from api.models import Marketplace

item_instance = Marketplace("ITEMS")
item_parser = reqparse.RequestParser()
item_parser.add_argument('item_name', help="This field cannot be blank", required=True)
item_parser.add_argument('item_quantity', help="this field cannot be blank", required=True)
order_instance = Marketplace("ORDERS")
order_parser = reqparse.RequestParser()
order_parser.add_argument('item_id', help='This field cannot be blank', required=True)
order_parser.add_argument('shop_id', help='This field cannot be blank', required=True)
shop_instance = Marketplace("SHOPS")


class OrderMap(Resource):
    @jwt_required
    def get(self):
        regular_user_id = get_jwt_identity()['regular_user_id']
        try:
            orders = order_instance.find_users_orders(ObjectId(regular_user_id))
            locations = []
            for order in orders:
                shop_details = shop_instance.find_shop_by_shop_id(order['shop_id'])
                locations.append(shop_details['shop_location'])
            return {'locations': locations}, 200
        except:
            return {'msg': 'Something went wrong'}, 500


class Order(Resource):
    @jwt_required
    def get(self):
        regular_user_id = get_jwt_identity()['regular_user_id']
        try:
            orders = order_instance.find_users_orders(ObjectId(regular_user_id))
            json_ready_orders = []
            for order in orders:
                shop_details = shop_instance.find_shop_by_shop_id(order['shop_id'])
                items = []
                for item in order['items']:
                    item_details = item_instance.find_item_by_id(ObjectId(item))
                    items.append(item_details['item_name'])

                order_item = {
                    'order_id': str(order['_id']),
                    'shop_id': str(order['shop_id']),
                    'shop_name': shop_details['shop_name'],
                    'items': items
                }
                json_ready_orders.append(order_item)
            return json_ready_orders, 200

        except:
            return {'msg': 'Something went wrong'}, 500

    @jwt_required
    def post(self):
        data = order_parser.parse_args()
        regular_user_id = get_jwt_identity()['regular_user_id']
        order = order_instance.find_order(ObjectId(data['shop_id']), ObjectId(regular_user_id))

        if not order:
            new_order = {
                'shop_id': ObjectId(data['shop_id']),
                'regular_user_id': ObjectId(regular_user_id),
                'created_at': datetime.datetime.now(),
                'items': [data['item_id'], ]
            }
            try:
                order_instance.save(new_order)
                return {'msg': 'new order created'}, 200
            except:
                return {'msg': 'Something went wrong'}, 500
        if order:
            updated_order = {
                'shop_id': ObjectId(data['shop_id']),
                'regular_user_id': ObjectId(regular_user_id),
                'updated_at': datetime.datetime.now(),
                'item': data['item_id']
            }
            try:
                order_instance.update_order(updated_order)
                return {'msg': 'your order was updated'}, 201
            except:
                return {'msg': 'Something went wrong'}, 500


class Item(Resource):
    def get(self):
        try:
            items = []
            for item in item_instance.find_items():
                item['_id'] = str(item['_id'])
                item['vendor_id'] = str(item['vendor_id'])
                item['shop_id'] = str(item['shop_id'])
                items.append(item)
            return items, 200
        except:
            return {'msg': 'Something went wrong'}, 500

    @jwt_required
    def post(self):
        data = item_parser.parse_args()
        vendor_id = get_jwt_identity()['vendor_id']
        shop_details = shop_instance.find_shop_by_vendor_id(ObjectId(vendor_id))
        item_details = item_instance.find_item_by_name(data['item_name'])
        # if shop does not exist
        if not shop_details:
            return {'msg': 'The current vendor\'s shop does not exists'}, 404
        # if item exists increment quantity
        if item_details:
            item_instance.increment_item_quantity(
                data['item_name'],
                ObjectId(vendor_id),
                int(data['item_quantity'])
            )
            return {'msg': 'Incremented item {0} by {1}'.format(
                data['item_name'],
                data['item_quantity']
            )}, 201

        new_item = {
            'item_name': data['item_name'],
            'item_quantity': int(data['item_quantity']),
            'vendor_id': ObjectId(vendor_id),
            'shop_id': shop_details['_id']
        }
        try:
            item_instance.save(new_item)
            return {'msg': 'item {} was successfully added'.format(data['item_name'])}, 201
        except:
            return {'msg': 'Something went wrong'}, 500
