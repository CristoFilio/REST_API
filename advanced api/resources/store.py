from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    not_found = {"message": "Store not found."}
    existing = "A store with name '{}' already exists. Please use a different name."
    error = {"message": "An error occurred while creating the store."}
    deleted = {"message": "Store deleted."}

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return Store.not_found, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': Store.existing.format(name)}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return Store.error, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return Store.deleted
        return Store.not_found, 404


class StoreList(Resource):
    def get(self):
        return {"stores": [x.json() for x in StoreModel.find_all()]}
