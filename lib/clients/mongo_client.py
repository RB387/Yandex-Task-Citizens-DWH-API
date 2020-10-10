from motor.motor_asyncio import AsyncIOMotorClient

from lib.clients.abstract_client import AbstractClient


class MongoClient(AsyncIOMotorClient, AbstractClient):
    """
        MongoClient based on AsyncIOMotorClient
        with AbstractClient interface realization

        Can be used only with one database what makes access to collection easier

        Usage:
            >>> uri = 'mongodb://localhost:27017'
            >>> db_name = 'some_database'
            >>> client = MongoClient(db_name, uri)
            >>> client['collection_name'].find_one({})
    """

    NAME = "mongo_client"

    def __init__(self, mongo_db_name, *args, **kwargs):
        self._mongo_db_name = mongo_db_name
        super().__init__(*args, **kwargs)

    def __getitem__(self, collection_name):
        database = AsyncIOMotorClient.__getitem__(self, self._mongo_db_name)
        return database[collection_name]
