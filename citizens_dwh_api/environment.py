import os

from citizens_dwh_api.entities.env_type import EnvType

ENV_TYPE = EnvType(os.environ["ENV_TYPE"])
PROD_MONGODB_URI = os.environ.get("PROD_MONGODB_URI")
DEV_MONGODB_URI = os.environ.get(
    "DEV_MONGODB_URI", "mongodb://127.0.0.1:10017/?replicaSet=dev-rs0"
)

if PROD_MONGODB_URI == DEV_MONGODB_URI:
    raise ValueError("Prod and dev mongodb shouldn't be the same")

if ENV_TYPE is EnvType.PROD:
    MONGODB_URI = PROD_MONGODB_URI
elif ENV_TYPE is EnvType.DEV:
    MONGODB_URI = DEV_MONGODB_URI
else:
    raise ValueError(f"Found unexpected environment {ENV_TYPE}")

if MONGODB_URI is None:
    raise ValueError("Mongodburi wasn't provided")
