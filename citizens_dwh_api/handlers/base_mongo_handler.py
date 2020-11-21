from motor.motor_asyncio import AsyncIOMotorClient

from simio.app.config_names import CLIENTS, VARS
from simio.handler.base import BaseHandler

from citizens_dwh_api.dto.mongo.dto import MongoCitizensDto


class DtoApiHandler(BaseHandler):
    @property
    def dto(self):
        return MongoCitizensDto(
            mongo_client=self.app[CLIENTS][AsyncIOMotorClient],
            db_name=self.app["config"][VARS]["mongo_db_name"],
            collection_name=self.app["config"][VARS]["mongo_collection_name"],
        )
