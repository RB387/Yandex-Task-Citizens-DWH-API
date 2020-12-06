from pathlib import Path

from simio.app.config_names import APP, CLIENTS, VARS
from motor.motor_asyncio import AsyncIOMotorClient

from citizens_dwh_api.environment import MONGODB_URI
from citizens_dwh_api.constants import MONGO_DB_NAME, MONGO_COLLECTION_NAME


def get_config():
    # fmt: off
    return {
        APP: {
            APP.name: "citizens_dwh_api",
            APP.version: "0.1.1",
            APP.handlers_path: Path(__file__).parent / "handlers",
        },
        CLIENTS: {
            AsyncIOMotorClient: {
                "host": MONGODB_URI,
            },
        },
        VARS: {
            "mongo_db_name": MONGO_DB_NAME,
            "mongo_collection_name": MONGO_COLLECTION_NAME
        }
    }
    # fmt: on
