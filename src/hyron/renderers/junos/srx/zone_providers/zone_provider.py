from abc import abstractmethod
from typing import Tuple, List
from plugable import Plugable
from .....helpers import get_plural_dict_item, as_list
from .....rules import Rule


class JunosSrxZoneProvider(Plugable):
    META_FROM_ZONE = "jsrx_from_zones"
    META_TO_ZONE = "jsrx_to_zones"

    def get_zones(self, rule: Rule):
        from_zones, to_zones = self._get_zones(rule)

        if self.META_FROM_ZONE in rule.metadata:
            from_zones = as_list(rule.metadata[self.META_FROM_ZONE])

        if self.META_TO_ZONE in rule.metadata:
            to_zones = as_list(rule.metadata[self.META_TO_ZONE])

        return (from_zones, to_zones)

    @classmethod
    def _get_explicit_zones(cls, meta: dict) -> bool:
        from_zones = get_plural_dict_item(meta, cls.META_FROM_ZONE)
        to_zones = get_plural_dict_item(meta, cls.META_TO_ZONE)

        return (from_zones, to_zones)

    @abstractmethod
    def _get_zones(self, rule) -> Tuple[List[str]]:
        pass


class DefaultJunosSrxZoneProvider(JunosSrxZoneProvider, register="default"):
    def _get_zones(self, rule):
        return ([], [])
