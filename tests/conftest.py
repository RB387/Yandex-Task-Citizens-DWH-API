from pathlib import Path
import uuid

import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from simio.app.config_names import CLIENTS, APP, VARS
from simio.app.builder import AppBuilder

from citizens_dwh_api.constants import MONGO_COLLECTION_NAME
from citizens_dwh_api.environment import DEV_MONGODB_URI


TEST_DB_NAME = "TEST_DATABASE_CITIZENS"


@pytest.fixture(scope="function")
def config():
    # fmt: off
    return {
        APP: {
            APP.name: "test_citizens_dwh_api",
            APP.handlers_path: Path(__file__).parent.parent / "citizens_dwh_api" / "handlers",
            APP.enable_swagger: False
        },
        CLIENTS: {
            AsyncIOMotorClient: {
                "host": DEV_MONGODB_URI,  # Use test mongo
            },
        },
        VARS: {
            "mongo_db_name": TEST_DB_NAME,
            "mongo_collection_name": MONGO_COLLECTION_NAME
        }
    }
    # fmt: on


@pytest.yield_fixture(scope="function")
def cli(config, loop, aiohttp_client):
    builder = AppBuilder(config)
    app = builder.build_app()

    yield loop.run_until_complete(aiohttp_client(app.app))

    loop.run_until_complete(
        app.app[CLIENTS][AsyncIOMotorClient].drop_database(TEST_DB_NAME)
    )


def patched_uuid():
    return uuid.UUID("3127989e-6e36-4710-b611-948deac76efe")
