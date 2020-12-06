import json

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
                    "citizen_id": "1",
                    "import_id": "id1",
                    "town": "СПБ",
                    "street": "Льва",
                    "building": "16к7стр3",
                    "apartment": "10",
                    "name": "Иванов Иваныч Иванович",
                    "birth_date": "01.02.1999",
                    "gender": "male",
                    "relatives": ["2"],
                },
                {
                    "citizen_id": "2",
                    "import_id": "id1",
                    "town": "Москва",
                    "street": "Льва Толстого",
                    "building": "16к7стр5",
                    "apartment": "7",
                    "name": "Да Да Да",
                    "birth_date": "01.02.2000",
                    "gender": "male",
                    "relatives": [1],
                },
                {
                    "citizen_id": "3",
                    "import_id": "id2",
                    "town": "Москва",
                    "street": "Льва Толстого",
                    "building": "16к7стр5",
                    "apartment": "7",
                    "name": "Другие Имя Фамилия",
                    "birth_date": "01.02.2000",
                    "gender": "male",
                    "relatives": [],
                },
            ],
            "id1",
            {
                "data": [
                    {
                        "citizen_id": "1",
                        "town": "СПБ",
                        "street": "Льва",
                        "building": "16к7стр3",
                        "apartment": "10",
                        "name": "Иванов Иваныч Иванович",
                        "birth_date": "01.02.1999",
                        "gender": "male",
                        "relatives": ["2"],
                    },
                    {
                        "citizen_id": "2",
                        "town": "Москва",
                        "street": "Льва Толстого",
                        "building": "16к7стр5",
                        "apartment": "7",
                        "name": "Да Да Да",
                        "birth_date": "01.02.2000",
                        "gender": "male",
                        "relatives": [1],
                    },
                ]
            },
            200,
        ),
        ([], "id1", {"data": []}, 200,),
    ),
)
@pytest.mark.asyncio
async def test_citizens_handler(
    cli, mongo_data, import_id, expected_response, expected_status
):
    if mongo_data:
        await cli.server.app[CLIENTS][AsyncIOMotorClient][TEST_DB_NAME][
            MONGO_COLLECTION_NAME
        ].insert_many(mongo_data)

    resp = await cli.get(f"/imports/{import_id}/citizens")

    # assert resp.status == expected_status
    assert json.loads(await resp.text()) == expected_response
