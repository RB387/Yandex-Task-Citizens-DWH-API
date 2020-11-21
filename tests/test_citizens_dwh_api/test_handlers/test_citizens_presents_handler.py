import json
from datetime import datetime

import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from simio.app.config_names import CLIENTS

from citizens_dwh_api.constants import MONGO_COLLECTION_NAME
from tests.conftest import TEST_DB_NAME


@pytest.mark.parametrize(
    "mongo_data, import_id, expected_response, expected_status",
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
                    "birth_date": datetime(2000, 2, 1, 0, 0),
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
                    "birth_date": datetime(2000, 5, 1, 0, 0),
                    "gender": "male",
                    "relatives": [1, 3],
                },
                {
                    "citizen_id": 3,
                    "import_id": "id1",
                    "town": "Москва",
                    "street": "Льва Толстого",
                    "building": "16к7стр5",
                    "apartment": "7",
                    "name": "Да Да Да",
                    "birth_date": datetime(2000, 9, 1, 0, 0),
                    "gender": "male",
                    "relatives": [2],
                },
                {
                    "citizen_id": 4,
                    "import_id": "id2",
                    "town": "Москва",
                    "street": "Льва Толстого",
                    "building": "16к7стр5",
                    "apartment": "7",
                    "name": "Другие Имя Фамилия",
                    "birth_date": datetime(2000, 3, 1, 0, 0),
                    "gender": "male",
                    "relatives": [],
                },
            ],
            "id1",
            {
                "data": {
                    "1": [],
                    "10": [],
                    "11": [],
                    "12": [],
                    "2": [{"citizen_id": 2, "presents": 1}],
                    "3": [],
                    "4": [],
                    "5": [
                        {"citizen_id": 1, "presents": 1},
                        {"citizen_id": 3, "presents": 1},
                    ],
                    "6": [],
                    "7": [],
                    "8": [],
                    "9": [{"citizen_id": 2, "presents": 1}],
                }
            },
            200,
        ),
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
                    "birth_date": datetime(2000, 2, 1, 0, 0),
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
                    "birth_date": datetime(2000, 5, 1, 0, 0),
                    "gender": "male",
                    "relatives": [1, 3],
                },
                {
                    "citizen_id": 3,
                    "import_id": "id1",
                    "town": "Москва",
                    "street": "Льва Толстого",
                    "building": "16к7стр5",
                    "apartment": "7",
                    "name": "Да Да Да",
                    "birth_date": datetime(1999, 2, 1, 0, 0),
                    "gender": "male",
                    "relatives": [2],
                },
            ],
            "id1",
            {
                "data": {
                    "1": [],
                    "10": [],
                    "11": [],
                    "12": [],
                    "2": [{"citizen_id": 2, "presents": 2}],
                    "3": [],
                    "4": [],
                    "5": [
                        {"citizen_id": 1, "presents": 1},
                        {"citizen_id": 3, "presents": 1},
                    ],
                    "6": [],
                    "7": [],
                    "8": [],
                    "9": [],
                }
            },
            200,
        ),
        (
            [],
            "id1",
            {
                "data": {
                    "1": [],
                    "10": [],
                    "11": [],
                    "12": [],
                    "2": [],
                    "3": [],
                    "4": [],
                    "5": [],
                    "6": [],
                    "7": [],
                    "8": [],
                    "9": [],
                }
            },
            200,
        ),
    ),
)
@pytest.mark.asyncio
async def test_citizens_presents_handler(
    cli, mongo_data, import_id, expected_response, expected_status
):
    if mongo_data:
        await cli.server.app[CLIENTS][AsyncIOMotorClient][TEST_DB_NAME][MONGO_COLLECTION_NAME].insert_many(
            mongo_data
        )

    resp = await cli.get(f"/imports/{import_id}/citizens/stat/birthdays")

    assert resp.status == expected_status
    assert json.loads(await resp.text()) == expected_response
