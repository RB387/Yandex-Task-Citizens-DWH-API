from aiohttp import web
from simio.handler.utils import route

from citizens_dwh_api.handlers.base_mongo_handler import DaoApiHandler
from citizens_dwh_api.handlers.utils import get_json_response


@route(path="/imports/{import_id}/towns/stat/percentile/age")
class PercentileAgeStatHandlerDao(DaoApiHandler):
    async def get(self, import_id: str) -> web.Response:
        percentile_stats = await self.dao.get_percentile_stats(import_id)

        return get_json_response(percentile_stats)
