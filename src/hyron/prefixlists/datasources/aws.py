from .web import WebPrefixListDatasource
from ...constants import AWS_IP_RANGES


class AwsPrefixListDatasource(WebPrefixListDatasource, register="aws"):
    def __init__(self, region=None, service=None):
        self._region = region
        self._service = service

        args = {
            "format": "json",
            "origin": AWS_IP_RANGES
        }

        super().__init__(**args)

    def _load_origin(self, origin):
        data = super()._load_origin(origin)

        prefixes = []

        prefixes += [pfx["ip_prefix"]
                     for pfx in data["prefixes"] if self._is_valid(pfx)]
        prefixes += [pfx["ipv6_prefix"]
                     for pfx in data["ipv6_prefixes"] if self._is_valid(pfx)]

        return prefixes

    def _is_valid(self, prefix):
        if self._region and prefix["region"] != self._region:
            return False
        if self._service and prefix["service"] != self._service:
            return False
        return True
