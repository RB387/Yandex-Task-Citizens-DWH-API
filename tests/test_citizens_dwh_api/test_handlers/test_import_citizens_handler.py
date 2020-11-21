import json

import pytest

from citizens_dwh_api.handlers.api import import_citizens_handler
from tests.conftest import patched_uuid


@pytest.mark.parametrize(
    "request_data, expected_response, expected_status",
    (
        (
            [
                {
                    "citizen_id": "3",
                    "town": "Москва",
                    "street": "Льва Толстого",
                    "building": "16к7стр5",
                    "apartment": "7",
                    "name": "Иванов Иван Иванович",
                    "birth_date": "01.02.2000",
                    "gender": "male",
                    "relatives": ["3"],
                }
            ],
            {"data": {"import_id": "3127989e-6e36-4710-b611-948deac76efe"}},
            201,
        ),
        (
            [
                {
                    "citizen_id": "dasds",
                    "town": 1,
                    "street": 22,
                    "building": 331,
                    "apartment": "7",
                    "name": 42342,
                    "birth_date": "not_date",
                    "gender": "not_enum",
                    "relatives": ["strange"],
                }
            ],
            {
                "error": {
                    "0": {
                        "birth_date": "value does not match format %d.%m.%Y",
                        "building": "value is not a string",
                        "citizen_id": "value can't be converted to int",
                        "gender": "value doesn't match any variant",
                        "name": "value is not a string",
                        "relatives": {"0": "value can't be converted to int"},
                        "street": "value is not a string",
                        "town": "value is not a string",
                    }
                }
            },
            400,
        ),
        (
            [
                {
                    "citizen_id": "3",
                    "town": "Москва",
                    "street": "Льва Толстого",
                    "building": "16к7стр5",
                    "apartment": "7",
                    "name": "Иванов Иван Иванович",
                    "birth_date": "01.02.2000",
                    "gender": "male",
                    "relatives": ["3"],
                },
                {
                    "citizen_id": "dasds",
                    "town": 1,
                    "street": 22,
                    "building": 331,
                    "apartment": "7",
                    "name": 42342,
                    "birth_date": "not_date",
                    "gender": "not_enum",
                    "relatives": ["strange"],
                },
            ],
            {
                "error": {
                    "1": {
                        "birth_date": "value does not match format %d.%m.%Y",
                        "building": "value is not a string",
                        "citizen_id": "value can't be converted to int",
                        "gender": "value doesn't match any variant",
                        "name": "value is not a string",
                        "relatives": {"0": "value can't be converted to int"},
                        "street": "value is not a string",
                        "town": "value is not a string",
                    }
                }
            },
            400,
        ),
    ),
)
@pytest.mark.asyncio
async def test_import_citizens_handler(
    cli, request_data, expected_response, expected_status, monkeypatch
):
    monkeypatch.setattr(import_citizens_handler, "uuid4", patched_uuid)
    resp = await cli.post("/imports", data=json.dumps(request_data))

    assert resp.status == expected_status
    assert json.loads(await resp.text()) == expected_response
