from pymongo import MongoClient


class MongoOperation:
    __client = None
    __database = None
    __collection = None

    def __init__(self, client_url: str, database_name: str, collection_name: str = None):
        self.client_url = client_url
        self.database_name = database_name
        self.collection_name = collection_name

    def create_client(self):
        if MongoOperation.__client is None:
            MongoOperation.__client = MongoClient(self.client_url)
        return MongoOperation.__client

    def create_database(self):
        if MongoOperation.__database is None:
            client = self.create_client()
            MongoOperation.__database = client[self.database_name]
        return MongoOperation.__database

    def create_collection(self):
        if MongoOperation.__collection is None:
            database = self.create_database()
            MongoOperation.__collection = database[self.collection_name]
        return MongoOperation.__collection

    def insert(self, data):
        collection = self.create_collection()
        if isinstance(data, list):
            collection.insert_many(data)
        else:
            collection.insert_one(data)

    def delete(self, filter):
        collection = self.create_collection()
        collection.delete_many(filter)

    def update(self, filter, update):
        collection = self.create_collection()
        collection.update_many(filter, update)

    def find(self, filter=None):
        collection = self.create_collection()
        if filter:
            return collection.find(filter)
        else:
            return collection.find_one()