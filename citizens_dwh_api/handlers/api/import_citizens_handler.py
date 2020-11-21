from uuid import uuid4

import trafaret as t
from aiohttp.web_response import Response
from simio.handler.utils import route

from citizens_dwh_api.handlers.base_mongo_handler import DtoApiHandler
from citizens_dwh_api.handlers.utils import get_json_response
from citizens_dwh_api.entities.schemas import Citizen


@route(path="/imports")
class ImportCitizensHandlerDto(DtoApiHandler):
    async def post(self, citizens: t.List(Citizen)) -> Response:
        import_id = str(uuid4())

        for citizen in citizens:
            citizen["import_id"] = import_id

        await self.dao.insert_many(citizens)
        return get_json_response({"import_id": import_id}, status=201)
