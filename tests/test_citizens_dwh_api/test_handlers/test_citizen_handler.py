import json
from datetime import datetime

import pytest
from simio.app.config_names import CLIENTS
from motor.motor_asyncio import AsyncIOMotorClient

from citizens_dwh_api.constants import MONGO_COLLECTION_NAME
from tests.conftest import TEST_DB_NAME


@pytest.mark.parametrize(
    "mongo_data, request_data, import_id, citizen_id, expected_patched_mongo_data, expected_response, expected_status",
    (
        (
            [
                {
                    "citizen_id": 1,
                    "import_id": "id1",
                    "town": "СПБ",
                    "street": "Льва",
                    "building": "16к7стр3",
                    "apartment": "10",
                    "name": "Иванов Иваныч Иванович",
                    "birth_date": datetime(1999, 2, 1, 0, 0),
                    "gender": "male",
                    "relatives": [2],
                },
                {
                    "citizen_id": 2,
                    "import_id": "id1",
                    "town": "Москва",
                    "street": "Льва Толстого",
                    "building": "16к7стр5",
                    "apartment": "7",
                    "name": "Да Да Да",
                    "birth_date": datetime(2000, 2, 1, 0, 0),
                    "gender": "male",
                    "relatives": [1],
                },
                {
                    "citizen_id": 3,
                    "import_id": "id1",
                    "town": "Москва",
                    "street": "Льва Толстого",
                    "building": "16к7стр5",
                    "apartment": "7",
                    "name": "Другие Имя Фамилия",
                    "birth_date": datetime(2000, 2, 1, 0, 0),
                    "gender": "male",
                    "relatives": [],
                },
            ],
            {
                "town": "Moscow",
                "street": "Льва Толстого",
                "building": "16к7стр6",
                "apartment": "133",
                "name": "Иванов Иван Иванович",
                "birth_date": "01.02.2000",
                "gender": "male",
                "relatives": [3],
            },
            "id1",
            1,
            [
                {
                    "citizen_id": 1,
                    "import_id": "id1",
                    "apartment": 133,
                    "birth_date": datetime(2000, 2, 1, 0, 0),
                    "building": "16к7стр6",
                    "gender": "male",
                    "name": "Иванов Иван Иванович",
                    "relatives": [3],
                    "street": "Льва Толстого",
                    "town": "Moscow",
                },
                {
                    "citizen_id": 2,
                    "import_id": "id1",
                    "town": "Москва",
                    "street": "Льва Толстого",
                    "building": "16к7стр5",
                    "apartment": "7",
                    "name": "Да Да Да",
                    "birth_date": datetime(2000, 2, 1, 0, 0),
                    "gender": "male",
                    "relatives": [],
                },
                {
                    "citizen_id": 3,
                    "import_id": "id1",
                    "town": "Москва",
                    "street": "Льва Толстого",
                    "building": "16к7стр5",
                    "apartment": "7",
                    "name": "Другие Имя Фамилия",
                    "birth_date": datetime(2000, 2, 1, 0, 0),
                    "gender": "male",
                    "relatives": [1],
                },
            ],
            {
                "data": {
                    "apartment": 133,
                    "birth_date": "01.02.2000",
                    "building": "16к7стр6",
                    "citizen_id": 1,
                    "gender": "male",
                    "name": "Иванов Иван Иванович",
                    "relatives": [3],
                    "street": "Льва Толстого",
                    "town": "Moscow",
                }
            },
            200,
        ),
    ),
)
@pytest.mark.asyncio
async def test_citizen_handler(
    cli,
    mongo_data,
    request_data,
    import_id,
    citizen_id,
    expected_patched_mongo_data,
    expected_response,
    expected_status,
):
    if mongo_data:
        await cli.server.app[CLIENTS][AsyncIOMotorClient][TEST_DB_NAME][MONGO_COLLECTION_NAME].insert_many(
            mongo_data
        )

    resp = await cli.patch(
        f"/imports/{import_id}/citizens/{citizen_id}", data=json.dumps(request_data)
    )

    assert resp.status == expected_status
    assert json.loads(await resp.text()) == expected_response

    cursor = cli.server.app[CLIENTS][AsyncIOMotorClient][TEST_DB_NAME][MONGO_COLLECTION_NAME].find(
        {}, {"_id": 0}
    )
    patched_mongo_data = [citizen async for citizen in cursor]

    assert patched_mongo_data == expected_patched_mongo_data
