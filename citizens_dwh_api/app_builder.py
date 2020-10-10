from typing import List, Type

from aiohttp import web
from aiohttp.web_routedef import RouteDef

from citizens_dwh_api.handlers.api.citizens_handler import CitizensHandler
from citizens_dwh_api.handlers.api.citizens_presents_handler.handler import (
    CitizensPresentsHandler,
)
from citizens_dwh_api.handlers.api.percentile_age_stat_handler.handler import (
    PercentileAgeStatHandler,
)
from citizens_dwh_api.handlers.api.import_citizens_handler import ImportCitizensHandler
from citizens_dwh_api.handlers.api.citizen_handler import CitizenHandler
from lib.app_builder import BaseAppBuilder
from lib.clients.abstract_client import AbstractClient
from lib.clients.mongo_client import MongoClient


class AppBuilder(BaseAppBuilder):
    @staticmethod
    def get_routes() -> List[RouteDef]:
        return [
            web.view("/imports", ImportCitizensHandler),
            web.view("/imports/{import_id}/citizens", CitizensHandler),
            web.view(
                "/imports/{import_id}/citizens/birthdays", CitizensPresentsHandler
            ),
            web.view("/imports/{import_id}/citizens/{citizen_id}", CitizenHandler),
            web.view(
                "/imports/{import_id}/towns/stat/percentile/age",
                PercentileAgeStatHandler,
            ),
        ]

    @staticmethod
    def get_clients() -> List[Type[AbstractClient]]:
        return [
            MongoClient,
        ]
