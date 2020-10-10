from json import JSONEncoder

from datetime import datetime

from citizens_dwh_api.constants import DATE_FORMAT


class DateTimeEncoder(JSONEncoder):
    def default(  # pylint: disable=inconsistent-return-statements
        self, obj
    ):  # pylint: disable=arguments-differ
        if isinstance(obj, datetime):
            return obj.strftime(DATE_FORMAT)
