from typing import List

from aiohttp.web_response import Response

from lib.handler.utils import get_request_args

from citizens_dwh_api.entities.schemas import Citizen
from citizens_dwh_api.handlers.base_mongo_handler import MongoApiHandler
from citizens_dwh_api.handlers.utils import get_json_response
from citizens_dwh_api.constants import MONGO_COLLECTION_NAME


class CitizensHandler(MongoApiHandler):
    @get_request_args(match_list=["import_id"])
    async def get(self, import_id: str) -> Response:
        citizens = await self._get_citizens(import_id)

        return get_json_response(citizens)

    async def _get_citizens(self, import_id) -> List[Citizen]:
        cursor = self.mongo[MONGO_COLLECTION_NAME].find(
            {"import_id": import_id}, {"_id": 0, "import_id": 0}
        )
        return [citizen async for citizen in cursor]
