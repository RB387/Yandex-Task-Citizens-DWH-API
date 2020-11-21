import json

from typing import Any
from simio.handler.utils import get_bad_request_exception

from aiohttp.web import json_response
from aiohttp.web_response import Response

from citizens_dwh_api.entities.exceptions import InputExceptions
from citizens_dwh_api.utils.json_encoder import DateTimeEncoder


def get_json_response(message: Any, status: int = 200) -> Response:
    data = json.dumps({"data": message}, cls=DateTimeEncoder)
    return json_response(data, status=status, dumps=lambda x: x)


def cast_citizen_id(citizen_id: Any) -> int:
    try:
        return int(citizen_id)
    except ValueError:
        raise get_bad_request_exception(InputExceptions.VALUE_ERROR.value)
