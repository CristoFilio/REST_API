from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.items import ItemModel


class Items(Resource):
    def get(self):
        items = [item.json() for item in ItemModel.query.all()]
        return {'items': items}, 201


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field is required.')
    parser.add_argument('store_id',
                        type=float,
                        required=True,
                        help='Every item needs a store id.')
    not_found = {'message': 'The item provided was not found.'}
    existing = {'message': 'That item already exists in inventory.'}
    created = 'Item has been added to the inventory successfully.'
    deleted = {'message': 'The item has been deleted from the inventory.'}
    updated = 'The item has been updated successfully.'
    error = {'message': 'There was a server error processing the item'}

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return Item.not_found, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return Item.existing, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return Item.error, 500
        return {'message': Item.created,
                'item': item.json()}, 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return Item.deleted, 200
        return Item.not_found, 404

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item:
            action = 'updated'
            code = 200
            item.price, item.store_id = data
        else:
            action = 'created'
            code = 201
            item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return Item.error, 500
        return {'message': f"Item has been {action}.",
                'item': item.json()}, code






























