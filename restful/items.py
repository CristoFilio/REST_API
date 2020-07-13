from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


class Items(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = cursor.execute('SELECT * FROM items')
        all_items = query.fetchall()
        connection.close()
        json_items = []
        for item in all_items:
            json_items.append({'id': item[0], 'name': item[1], 'price': item[2]})
        return {'items': json_items}, 201


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field is required.")
    not_found = {'message': "The item provided was not found."}
    existing = {'message': "That item already exists in inventory."}
    created = "Item has been added to the inventory successfully."
    deleted = {'message': "The item has been deleted from the inventory."}
    updated = "The item has been updated successfully."
    server_error = {'message': 'There was a server error and your request could'
                               'not be processed'}

    def db_connect(self, action, name=None, data=None):
        # Find the item using the name.
        if action == 'find':
             action = f"SELECT * FROM items WHERE name='{name}'"
        # Create an item using the name and price.
        elif action == 'create':
            action = f"INSERT INTO items VALUES (NULL, '{name}', {data['price']})"
        # Find the item using the name and update the price.
        elif action == 'update':
            action = f"UPDATE items SET price = {data['price']} WHERE name ='{name}'"
        # Delete the item using the name
        elif action == 'delete':
            action = f"DELETE FROM items WHERE name='{name}'"
        try:
            # Create connection and cursor.
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            # Execute the action.
            query = cursor.execute(action)
            # Get the value where the cursor is and set as item.
            item = query.fetchone()
            # Close connection and return item.
            connection.commit()
            connection.close()
            return item
        except:
            return Item.server_error, 500
        finally:
            connection.close()

    @jwt_required()
    def get(self, name):
        item = self.db_connect('find', name)
        if item:
            return {'item': {'id': item[0], 'name': item[1], 'price': item[2]}}, 200
        return Item.not_found, 404

    def post(self, name):
        if self.db_connect('find', name):
            return Item.existing, 400
        data = Item.parser.parse_args()
        self.db_connect('create', name, data['price'])
        item = self.db_connect('find', name)
        return {'message': Item.created,
                'item': {'id': item[0], 'name': item[1], 'price': item[2]}}, 201

    def delete(self, name):
        item = self.db_connect('find', name)
        if item:
            self.db_connect('delete', name)
            return Item.deleted, 200
        return Item.not_found, 404

    def put(self, name):
        data = Item.parser.parse_args()
        item = self.db_connect('find', name)
        if item:
            self.db_connect('update', name, data)
            item = self.db_connect('find', name)
            return {'message': Item.updated,
                    'item': {'id': item[0], 'name': item[1], 'price': item[2]}}, 200
        self.db_connect('create', name, data)
        item = self.db_connect('find', name)
        return {'message': Item.created,
                'item': {'id': item[0], 'name': item[1], 'price': item[2]}}, 201






























