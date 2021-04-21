from typing import List
from collections import defaultdict

from .datastructures import \
    JunosSrxAddress, \
    JunosSrxAddressSet, \
    JunosSrxApplication, \
    JunosSrxRule

from .zone_providers import JunosSrxZoneProvider
from ...renderer import Renderer
from ....apps import Application
from ....rules import Rule


class JunosSrxRenderer(Renderer):
    META_CONTEXT = "jsrx_context"

    def __init__(self, **config):
        super().__init__(**config)
        self.addresses = {}
        self.address_sets = {}
        self.applications = {}

        self.global_policies = []
        self.zonal_policies = defaultdict(lambda: defaultdict(lambda: []))

        self.zone_provider = self._get_zone_provider()

    def _get_zone_provider(self) -> JunosSrxZoneProvider:
        return JunosSrxZoneProvider.get(
            self.config.get(
                "jsrx-zone-provider",
                "default"))

    def build_address_object(self, prefix: str) -> str:
        address = JunosSrxAddress.get_for_prefix(prefix, self.addresses)
        return address.name

    def build_address_set_object(
            self,
            set_name,
            address_names: List[str]) -> str:
        address_set = JunosSrxAddressSet(set_name, address_names)
        self.address_sets[set_name] = address_set
        return address_set.name

    def _initialise(self):
        self.preprocess_entities = True

    def _preprocess_prefix_list(self, pfx_list):
        names = [self.build_address_object(pfx) for pfx in pfx_list.prefixes]
        self.build_address_set_object(pfx_list.name, names)

    def _preprocess_app(self, app: Application):
        if "jsrx-app" not in app.metadata:
            junos_app = JunosSrxApplication.from_app(app)
            self.applications[app.name] = junos_app
            return app.name
        return app.metadata["jsrx-app"]

    def _process_rule(self, rule: Rule):
        apps = []

        for app in rule.applications.apps:
            if "jsrx-app" in app.metadata:
                apps.append(app.metadata["jsrx-app"])
            else:
                apps.append(self.applications[app.name].name)

        junos_rule = JunosSrxRule(
            rule.name,
            self.address_sets[rule.source.name].name,
            self.address_sets[rule.destination.name].name,
            apps,
            rule.action
        )

        if rule.metadata.get(self.META_CONTEXT, "zonal") == "global":
            junos_rule.force_global = True

        from_zones, to_zones = self.zone_provider.get_zones(rule)

        if from_zones:
            junos_rule.from_zones = from_zones

        if to_zones:
            junos_rule.to_zones = to_zones

        ctx = "global"
        seq = len(self.global_policies) + 1
        policy_list = self.global_policies

        if not junos_rule.is_global:
            policy_list = self.zonal_policies[from_zones[0]][to_zones[0]]
            ctx = f"{from_zones[0]}_{to_zones[0]}"
            seq = len(policy_list) + 1

        junos_rule.name = f"{ctx}_{seq}"

        policy_list.append(junos_rule)

    def get_sorted_objects(self):
        apps = list(self.applications.keys())
        addresses = list(self.addresses.keys())
        address_sets = list(self.address_sets.keys())

        apps.sort()
        addresses.sort()
        address_sets.sort()

        def _map(keys, dct):
            return map(lambda x: dct[x], keys)

        return (
            _map(apps, self.applications),
            _map(addresses, self.addresses),
            _map(address_sets, self.address_sets)
        )

    def get_sorted_zone_pairs(self):
        from_zones = list(self.zonal_policies.keys())
        from_zones.sort()

        for from_zone in from_zones:
            to_zones = list(self.zonal_policies[from_zone].keys())
            to_zones.sort()

            for to_zone in to_zones:
                yield (from_zone, to_zone)
