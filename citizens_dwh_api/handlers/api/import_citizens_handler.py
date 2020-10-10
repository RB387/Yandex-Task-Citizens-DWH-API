from typing import List
from uuid import uuid4

import trafaret as t
from aiohttp.web_response import Response

from citizens_dwh_api.handlers.base_mongo_handler import MongoApiHandler
from citizens_dwh_api.handlers.utils import get_json_response
from citizens_dwh_api.constants import MONGO_COLLECTION_NAME
from citizens_dwh_api.entities.schemas import Citizen
from lib.handler.utils import validate_request_schema


class ImportCitizensHandler(MongoApiHandler):
    request_schema: t.Trafaret = t.List(Citizen)

    @validate_request_schema(request_schema)
    async def post(self, request_json: List[Citizen]) -> Response:
        import_id = str(uuid4())

        for citizen in request_json:
            citizen["import_id"] = import_id

        await self.mongo[MONGO_COLLECTION_NAME].insert_many(request_json)
        return get_json_response({"import_id": import_id}, status=201)
