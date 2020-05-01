from typing import List
from .rule import Rule
from ..prefixlists.prefix_list import PrefixList


class RuleSet:
    def __init__(self, rules=[], **meta):
        self.rules: List[Rule] = rules
        self.metadata = meta

    @property
    def prefix_lists(self) -> List[PrefixList]:
        pfx_lists = []
        for lists in map(lambda x: x.prefix_lists, self.rules):
            for pfx_list in lists:
                if pfx_list not in pfx_lists:
                    pfx_lists.append(pfx_list)
        return pfx_lists

    @property
    def applications(self):
        apps = []
        for appcontainer in map(lambda x: x.applications, self.rules):
            for app in appcontainer.apps:
                if app not in apps:
                    apps.append(app)
        return apps
