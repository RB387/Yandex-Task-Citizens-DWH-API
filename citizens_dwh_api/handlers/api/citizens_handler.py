from simio.handler.utils import route

from aiohttp.web_response import Response

from citizens_dwh_api.handlers.base_mongo_handler import DaoApiHandler
from citizens_dwh_api.handlers.utils import get_json_response


@route(path="/imports/{import_id}/citizens")
class CitizensHandlerDao(DaoApiHandler):
    async def get(self, import_id: str) -> Response:
        raw_citizens = await self.dao.get_citizens_by_import_id(import_id)

        return get_json_response(raw_citizens)
