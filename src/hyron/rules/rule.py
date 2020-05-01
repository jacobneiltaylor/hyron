from typing import List
from ..constants import ACTION_PERMIT
from ..prefixlists.prefix_list import PrefixList
from ..apps.application import ApplicationContainer


class Rule:
    def __init__(
            self,
            src: PrefixList,
            dst: PrefixList,
            apps: ApplicationContainer,
            action=ACTION_PERMIT,
            **meta):
        self.source = src
        self.destination = dst
        self.applications = apps
        self.action = action
        self.metadata = meta

    @property
    def prefix_lists(self) -> List[PrefixList]:
        return [self.source, self.destination]

    @property
    def name(self) -> str:
        if "name" in self.metadata:
            return self.metadata["name"]
        app = self.applications.name
        src = self.source.name
        dst = self.destination.name
        return f"{self.action}_{app}_from_{src}_to_{dst}"
