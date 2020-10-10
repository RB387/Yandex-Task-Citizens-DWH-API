from lib.clients.mongo_client import MongoClient
from lib.handler.api_handler import ApiHandler


class MongoApiHandler(ApiHandler):
    @property
    def mongo(self):
        return self.app[MongoClient.NAME]
