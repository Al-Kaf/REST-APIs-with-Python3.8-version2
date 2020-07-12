import sqlite3
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from models.store import StoreModel


class Store(Resource):

    @jwt_required
    def get(self, name):
        store = StoreModel.find_item_by_name(name)
        if store:
            return store.json()
        return {"massage": " store Not found"}, 404

    def post(self, name):

        if StoreModel.find_item_by_name(name):
            return {"message": "An store with name '{}' already exists.".format(name)}, 400  # 400 for bad requst

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred when add store."}, 500  # 500 > internal Server error

        return store.json(), 201  # 201 is the number for creat

    def delete(self, name):
        store = StoreModel.find_item_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": "store deleted"}
        return {"message": "store NOT found"}



class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.find_all()]}
