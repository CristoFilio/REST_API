from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):

    existing = {'message': 'This store already exists'}
    created = {'message': 'The store was successfully created'}
    deleted = {'message': 'The store was successfully deleted'}
    not_found = {'message': 'This store does not exists'}
    error = {'message': 'There was a server error while processing your request'}

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return Store.created, store.json, 200
        return Store.not_found, 404

    def post(self, name):
        store = StoreModel(name)
        if store.find_by_name(name):
            return Store.existing, 400
        try:
            store.save_to_db()
        except:
            Store.error, 500
        return Store.created, 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_db()
            except:
                Store.error, 500
            return Store.deleted, 200
        return Store.not_found, 404


class StoreList(Resource):
    def get(self):
        stores = [store.json() for store in StoreModel.query.all()]
        return {'stores': stores}

