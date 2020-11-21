from aiohttp import web
from simio.handler.utils import route

from citizens_dwh_api.handlers.base_mongo_handler import DtoApiHandler
from citizens_dwh_api.handlers.utils import get_json_response


@route("/imports/{import_id}/citizens/stat/birthdays")
class CitizensPresentsHandlerDto(DtoApiHandler):
    async def get(self, import_id: str) -> web.Response:
        percentile_stats = await self.dto.get_presents_stat(import_id)
        return get_json_response(percentile_stats)
