from typing import Dict, Any

from aiohttp import web
from more_itertools import one

from lib.handler.utils import get_request_args
from citizens_dwh_api.constants import MONGO_COLLECTION_NAME
from citizens_dwh_api.handlers.api.citizens_presents_handler.presents_aggregation import (
    PresentsAggregation,
)
from citizens_dwh_api.handlers.base_mongo_handler import MongoApiHandler
from citizens_dwh_api.handlers.utils import get_json_response


class CitizensPresentsHandler(MongoApiHandler):
    @get_request_args(match_list=["import_id"])
    async def get(self, import_id: str) -> web.Response:
        percentile_stats = await self.get_presents_stat(import_id)
        return get_json_response(percentile_stats)

    async def get_presents_stat(self, import_id: str) -> Dict[str, Any]:
        aggregation = PresentsAggregation(import_id)
        cursor = self.mongo[MONGO_COLLECTION_NAME].aggregate(aggregation.get())

        return one([presents_stat async for presents_stat in cursor])
