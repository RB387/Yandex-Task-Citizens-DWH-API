from citizens_dwh_api.environment import MONGODB_URI
from citizens_dwh_api.constants import MONGO_DB_NAME
from lib.clients.mongo_client import MongoClient


def get_config():
    # fmt: off
    return {
        # --- clients ---
        MongoClient.NAME: {
            "host": MONGODB_URI,
            "mongo_db_name": MONGO_DB_NAME
        }
    }
    # fmt: on
