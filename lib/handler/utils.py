import json
from typing import Any, Dict
from typing import List, Optional as Opt, Callable
import trafaret as t
from aiohttp.web_exceptions import HTTPBadRequest


def get_bad_request_exception(message: Any) -> HTTPBadRequest:
    body = {"error": message}
    return HTTPBadRequest(reason="Bad Request", body=json.dumps(body))


def validate_request_data(data: str) -> Any:
    try:
        return json.loads(data)
    except json.decoder.JSONDecodeError:
        raise get_bad_request_exception("Incorrect data")


def validate_request_schema(
    schema: t.Trafaret,
    exception_handler: Callable[
        [Dict[str, str]], HTTPBadRequest
    ] = get_bad_request_exception,
):
    """
    Decorator for request schema validation for class based aiohttp views

    If request schema is correct, then adds kwarg `request_json` with casted dict to function
    that uses this decorator
    If request schema is wrong, raises 400 Bad Request error

    Usage:
        >>> request_schema = t.Dict({t.Key('key'):t.ToInt(gt=0),})
        >>>
        >>> @validate_request_schema(request_schema):
        ... async def some_handler(self, request_json)

    :param schema: schema that should be checked for request
    :param exception_handler: function to handle schema exception.
                              Takes one argument which is dictionary with reason
                              why schema was incorrect
                              Should return aiohttp.web.HTTPBadRequest.
    """

    def decorator(func):
        async def wrapper(self, *args, **kwargs):
            try:
                json_data = validate_request_data(await self.request.text())
                validated_data = schema.check(json_data)
                return await func(self, *args, *kwargs, request_json=validated_data)
            except t.DataError as exception:
                raise exception_handler(exception.as_dict())

        return wrapper

    return decorator


def get_request_args(
    match_list: Opt[List[str]] = None, query_list: Opt[List[str]] = None
):
    """
        Decorator to get args from aiohttp dynamic urls
        Usage:
            >>> url = 'http://url.com/{user}?q1=data&q2=data2'
            >>> @get_request_args(match_list=['user',], query_list=['q1', 'q2'])
            ... async def some_handler(self, user, q1, q2):

        :param match_list: list with args that used in dynamic url
        :param query_list: list with args that used in url query
        """

    def decorator(func):
        def wrapper(self, *args, **kwargs):
            for match_arg in match_list or []:
                kwargs[match_arg] = self.request.match_info.get(match_arg)
            for query_arg in query_list or []:
                kwargs[query_arg] = self.request.query.get(query_arg)
            return func(self, *args, **kwargs)

        return wrapper

    return decorator
