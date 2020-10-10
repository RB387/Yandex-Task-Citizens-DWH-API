from aiohttp import web
from trafaret import Trafaret, Dict


class ApiHandler(web.View):
    """
    Base class of api handler

    Properties:
        :app: current aiohttp app
        :config: config of app
        :request_schema: trafaret for request schema validation if needed.
                         Use with decorator `validate_request_schema` from utils
    """

    request_schema: Trafaret = Dict()

    @property
    def app(self) -> web.Application:
        return self.request.app

    @property
    def config(self) -> dict:
        return self.app["config"]
