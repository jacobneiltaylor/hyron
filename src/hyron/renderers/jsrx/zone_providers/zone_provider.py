from abc import abstractmethod
from typing import Tuple, List
from plugable import Plugable
from ....helpers import get_plural_dict_item, as_list


class JunosSrxZoneProvider(Plugable):
    META_CONTEXT = "jsrx_context"
    META_FROM_ZONE = "jsrx_from_zones"
    META_TO_ZONE = "jsrx_to_zones"

    def is_global(self, rule) -> bool:
        from_zones, to_zones = self.get_zones(rule)

        if len(from_zones) != 1 or len(to_zones) != 1:
            return True

        if self.META_CONTEXT in rule.metadata:
            context = rule.metadata[self.META_CONTEXT]
            if context == "global":
                return True
            else:
                assert(len(from_zones) == 1 and len(to_zones) == 1)
                return False

        return self._is_global(rule)

    def get_zones(self, rule):
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
    def _is_global(self, rule) -> bool:
        pass

    @abstractmethod
    def _get_zones(self, rule) -> Tuple[List[str]]:
        pass


class DefaultJunosSrxZoneProvider(JunosSrxZoneProvider, register="default"):
    def _is_global(self, rule):
        return True

    def _get_zones(self, rule):
        return ([], [])
