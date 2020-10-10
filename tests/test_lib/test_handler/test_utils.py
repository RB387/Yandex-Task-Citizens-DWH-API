import pytest

import json
import trafaret as t
from aiohttp.web_exceptions import HTTPBadRequest
from yarl import URL

from lib.handler.utils import (
    validate_request_data,
    validate_request_schema,
    get_request_args,
)
from tests.mocks import RequestMock


@pytest.mark.parametrize(
    "input_data, expected_json, expected_exception_type",
    (
        (
            '{"key": "value", "another_key": 1337}',
            {"key": "value", "another_key": 1337},
            None,
        ),
        ("bad_json", None, HTTPBadRequest,),
    ),
)
def test_validate_request_data(input_data, expected_json, expected_exception_type):
    try:
        result = validate_request_data(input_data)
        assert result == expected_json
    except Exception as exception:
        assert type(exception) == expected_exception_type


@pytest.mark.parametrize(
    "schema, request_data, expected_json, expected_exception_message",
    (
        (
            t.Dict({t.Key("key1"): t.ToInt(gt=0), t.Key("key2"): t.Enum(1, 2),}),
            '{"key1": 1, "key2": 2}',
            {"key1": 1, "key2": 2},
            None,
        ),
        (
            t.Dict({t.Key("key1"): t.ToInt(gt=0), t.Key("key2"): t.Enum(1, 2),}),
            '{"key1": 0, "key2": -1}',
            None,
            {
                "error": {
                    "key1": "value should be greater than 0",
                    "key2": "value doesn't match any variant",
                }
            },
        ),
    ),
)
@pytest.mark.asyncio
async def test_validate_request_schema(
    schema, request_data, expected_json, expected_exception_message
):
    class Handler:
        request = RequestMock(data=request_data)

        @validate_request_schema(schema)
        async def func(self, request_json):
            return request_json

    handler = Handler()
    try:
        result = await handler.func()
        assert result == expected_json
    except HTTPBadRequest as exception:
        assert json.loads(exception.body._value) == expected_exception_message


@pytest.mark.parametrize(
    "match_list, query_list, url, expected_kwargs",
    (
        (
            ["user_id", "page_num"],
            ["category", "filter"],
            URL(
                "http://test.com/{user_id:1337}/files/{page_num:2}?category=important&filter=pr:2"
            ),
            {
                "user_id": "1337",
                "page_num": "2",
                "category": "important",
                "filter": "pr:2",
            },
        ),
    ),
)
def test_get_request_args(match_list, query_list, url, expected_kwargs):
    class Handler:
        request = RequestMock(url=url)

        @get_request_args(match_list=match_list, query_list=query_list)
        def func(self, **kwargs):
            return kwargs

    result = Handler().func()

    assert result == expected_kwargs
