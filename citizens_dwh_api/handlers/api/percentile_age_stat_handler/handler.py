from typing import Any, Dict, List

from aiohttp import web

from lib.handler.utils import get_request_args
from citizens_dwh_api.constants import PERCENTILES, MONGO_COLLECTION_NAME
from citizens_dwh_api.handlers.api.percentile_age_stat_handler.percentile_aggregation import (
    PercentileAggregation,
)
from citizens_dwh_api.handlers.base_mongo_handler import MongoApiHandler
from citizens_dwh_api.handlers.utils import get_json_response


class PercentileAgeStatHandler(MongoApiHandler):
    @get_request_args(match_list=["import_id"])
    async def get(self, import_id: str) -> web.Response:
        percentile_stats = await self.get_percentile_stats(import_id)

        return get_json_response(percentile_stats)

    async def get_percentile_stats(self, import_id: str) -> List[Dict[str, Any]]:
        aggregation = PercentileAggregation(PERCENTILES, import_id)
        cursor = self.mongo[MONGO_COLLECTION_NAME].aggregate(aggregation.get())
        return [city_stat async for city_stat in cursor]
