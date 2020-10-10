from urllib.parse import unquote


class RequestMock:
    def __init__(self, data=None, url=None):
        self.data = data
        self.url = url
        self.match_info = None
        self.query = None

        if url is not None:
            self.query = url.query
            self.match_info = self._get_info_from_url()

    def _get_info_from_url(self):
        match_info = {}
        unquote_url = unquote(str(self.url.path))

        for part in unquote_url.split("/"):
            if part.startswith("{") and part.endswith("}"):
                content = part[1 : len(part) - 1]
                key, value = content.split(":")
                match_info[key] = value

        return match_info

    async def text(self):
        return self.data
