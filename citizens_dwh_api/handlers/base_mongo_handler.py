from motor.motor_asyncio import AsyncIOMotorClient

from simio.app.config_names import CLIENTS, VARS
from simio.handler.base import BaseHandler

from citizens_dwh_api.dao.mongo.dao import MongoCitizensDao


class DaoApiHandler(BaseHandler):
    @property
    def dao(self):
        return MongoCitizensDao(
            mongo_client=self.app[CLIENTS][AsyncIOMotorClient],
            db_name=self.app["config"][VARS]["mongo_db_name"],
            collection_name=self.app["config"][VARS]["mongo_collection_name"],
        )
