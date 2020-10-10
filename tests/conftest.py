import uuid

import pytest

from citizens_dwh_api.app_builder import AppBuilder
from citizens_dwh_api.environment import DEV_MONGODB_URI
from lib.clients.mongo_client import MongoClient


TEST_DB_NAME = "TEST_DATABASE_CITIZENS"


@pytest.fixture(scope="function")
def config():
    # fmt: off
    return {
        # --- clients ---
        MongoClient.NAME: {
            "host": DEV_MONGODB_URI,  # Use test mongo
            "mongo_db_name": TEST_DB_NAME
        }
    }
    # fmt: on


@pytest.yield_fixture(scope="function")
def cli(config, loop, aiohttp_client):
    builder = AppBuilder(config)
    app = builder.build_app()

    yield loop.run_until_complete(aiohttp_client(app))

    loop.run_until_complete(app[MongoClient.NAME].drop_database(TEST_DB_NAME))


def patched_uuid():
    return uuid.UUID("3127989e-6e36-4710-b611-948deac76efe")
