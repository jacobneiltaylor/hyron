import json
import requests

from ..prefix_list_datasource import PrefixListDatasource
from ...helpers import get_plural_dict_item


class WebPrefixListDatasource(PrefixListDatasource, register="web"):
    FORMAT_HANDLERS = {
        "text": lambda x: [
            i for i in map(
                lambda y: y.strip(),
                x.splitlines()) if i[0] != "#"],
        "csv": lambda x: x.strip().split(","),
        "json": lambda x: json.loads(x)}

    def __init__(self, **kwargs):
        self._origins = get_plural_dict_item(kwargs, "origin")
        self._format = kwargs["format"]
        self._session = requests.Session()

    def _load_origin(self, origin):
        response = self._session.get(origin)
        encoding = response.apparent_encoding
        raw = response.content.decode(encoding)
        return self.FORMAT_HANDLERS[self._format](raw)

    def fetch(self):
        prefixes = []
        for origin in self._origins:
            prefixes += self._load_origin(origin)
        return prefixes
