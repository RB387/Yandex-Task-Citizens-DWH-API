from typing import List, Type

from aiohttp import web
from aiohttp.web_routedef import RouteDef

from lib.clients.abstract_client import AbstractClient


class BaseAppBuilder:
    """
    Base class with app builder
    Set ups all app's routes and registers all clients

    Takes positional argument config in __init__ with app configuration
    Config should contain all required information for client initialization
    that can be accesed by key: client.NAME

    Example of config:
        config = {
            # --- clients ---
            AbstractClient.NAME: {
                'host': 'localhost',
                'port': 27017
            }
            # --- app config ---
            'any_key': 'any_value'
        }

    Public methods for usage:
        build_app() -> web.Application
            :returns aiohttp web application

    You should realize `get_routes` method to setup routes for your app
    You should realize `get_clients` method to register client for your app

    Example of registered clients usage:
        :app[client.NAME]:
    """

    def __init__(self, config=None):
        if config is None:
            config = {}
        self._config = config

    def build_app(self) -> web.Application:
        app = web.Application()
        app["config"] = self._config
        app.add_routes(self.get_routes())
        self._register_clients(app)

        return app

    @staticmethod
    def get_routes() -> List[RouteDef]:
        """
        Register here your app's routes

        Example:
            >>>return [
            ...    web.view('path/{to}/handler', Handler),
            ...    web.view('another/path', AnotherHandler)
            ...]

        :return: list with app's routes
        """
        return []

    @staticmethod
    def get_clients() -> List[Type[AbstractClient]]:
        """
        Register here your app's client with AbstractClient interface

        Example:
            >>>return [
            ...    MongoClient,
            ...    RedisClient
            ...]

        :return: list with app's clients
        """

        return []

    def _register_clients(self, app: web.Application):
        for client in self.get_clients():
            client_kwargs = self._config[client.NAME]
            app[client.NAME] = client(**client_kwargs)
