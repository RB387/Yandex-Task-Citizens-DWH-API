from motor.motor_asyncio import AsyncIOMotorClient
from unittest.mock import patch

import json
import pytest
from datetime import datetime
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
                    "birth_date": datetime(1980, 5, 1, 0, 0),
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
                    "birth_date": datetime(1999, 9, 1, 0, 0),
                    "gender": "male",
                    "relatives": [2],
                },
                {
                    "citizen_id": 4,
                    "import_id": "id1",
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
                "data": [
                    {"p50": 21.13, "p75": 40.47, "p99": 40.47, "town": "Москва"},
                    {"p50": 21.71, "p75": 21.71, "p99": 21.71, "town": "СПБ"},
                ]
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
                    "town": "Самара",
                    "street": "Льва Толстого",
                    "building": "16к7стр5",
                    "apartment": "7",
                    "name": "Да Да Да",
                    "birth_date": datetime(1984, 5, 1, 0, 0),
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
                    "birth_date": datetime(1969, 2, 1, 0, 0),
                    "gender": "male",
                    "relatives": [2],
                },
            ],
            "id1",
            {
                "data": [
                    {"p50": 51.73, "p75": 51.73, "p99": 51.73, "town": "Москва"},
                    {"p50": 20.71, "p75": 20.71, "p99": 20.71, "town": "СПБ"},
                    {"p50": 36.47, "p75": 36.47, "p99": 36.47, "town": "Самара"},
                ]
            },
            200,
        ),
        ([], "id1", {"data": []}, 200,),
    ),
)
@pytest.mark.asyncio
async def test_percentile_age_stat_handler(
    cli, mongo_data, import_id, expected_response, expected_status,
):
    if mongo_data:
        await cli.server.app[CLIENTS][AsyncIOMotorClient][TEST_DB_NAME][MONGO_COLLECTION_NAME].insert_many(
            mongo_data
        )
    with patch('citizens_dwh_api.dto.mongo.percentile_aggregation.datetime') as mock:
        mock.now.return_value = datetime(year=2020, month=10, day=11)
        resp = await cli.get(f"/imports/{import_id}/towns/stat/percentile/age")

    assert resp.status == expected_status
    assert json.loads(await resp.text()) == expected_response
