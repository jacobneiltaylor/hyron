import json
from copy import deepcopy
from typing import List
from ipaddress import ip_network
from collections import defaultdict
from .zone_providers import JunosSrxZoneProvider
from ..renderer import Renderer
from ...apps import Application, PortApplication
from ...rules import Rule
from ...constants import ACTION_PERMIT, ACTION_REJECT, ACTION_IGNORE


def _permit_handler(renderer):
    if "jsrx-configure-permit" in renderer.metadata:
        return renderer.metadata["jsrx-configure-permit"]
    return [None]


_ACTION_MAP = {
    ACTION_PERMIT: ("permit", _permit_handler),
    ACTION_REJECT: ("reject", lambda x: [None]),
    ACTION_IGNORE: ("deny", lambda x: [None])
}


class JunosSrxRenderer(Renderer, register="jsrx"):
    def __init__(self, **config):
        super().__init__(**config)
        self.address_objects = []
        self.address_set_objects = []
        self.application_objects = []

        self.address_index = set()
        self.address_set_index = {}
        self.application_index = {}

        self.global_policies = []
        self.zonal_policies = defaultdict(lambda: defaultdict(lambda: []))

        self.zone_provider = self._get_zone_provider()

    def _get_zone_provider(self) -> JunosSrxZoneProvider:
        return JunosSrxZoneProvider.get(
            self.config.get(
                "jsrx-zone-provider",
                "default"))

    def build_address_object(self, prefix: str) -> str:
        net = ip_network(prefix)
        name = f"pfx{net.version}-{net.network_address.compressed}-{net.prefixlen}"  # noqa

        if name not in self.address_index:
            address_object = {
                "name": name,
                "ip-prefix": net.exploded
            }
            self.address_objects.append(address_object)
            self.address_index.add(name)

        return name

    def build_address_set_object(
            self,
            set_name,
            address_names: List[str]) -> str:
        address_set_object = {
            "name": set_name,
            "address": [{"name": name} for name in address_names]
        }
        self.address_set_objects.append(address_set_object)
        return address_set_object["name"]

    def build_application_object(self, app: Application):
        if "jsrx-app" not in app.metadata:
            app_object = {
                "name": app.name,
                "protocol": app.protocol,
            }

            if isinstance(app, PortApplication):
                dst = str(app.from_port)
                if app.from_port != app.to_port:
                    dst = f"{dst}-{app.to_port}"
                app_object["destination-port"] = dst

            self.application_objects.append(app_object)
            return app.name
        return app.metadata["jsrx-app"]

    def build_policy_then(self, action):
        then = {}

        key, value_func = _ACTION_MAP[action]
        then[key] = value_func(self)

        # TODO: Add metadata checks for log/count

        return then

    def build_policy_match(self, src: str, dst: str, apps):
        return {
            "source-address": [self.address_set_index[src]],
            "destination-address": [self.address_set_index[dst]],
            "application": [self.application_index[app] for app in apps]
        }

    def _initialise(self):
        self.preprocess_entities = True

    def _preprocess_prefix_list(self, pfx_list):
        names = [self.build_address_object(pfx) for pfx in pfx_list.prefixes]
        self.address_set_index[pfx_list.name] = self.build_address_set_object(
            pfx_list.name, names)

    def _preprocess_app(self, app):
        self.application_index[app.name] = self.build_application_object(app)

    def _process_rule(self, rule: Rule):
        from_zones, to_zones = self.zone_provider.get_zones(rule)

        is_global = self.zone_provider.is_global(rule)
        ctx = "global"
        seq = len(self.global_policies) + 1

        app_names = map(lambda x: x.name, rule.applications.apps)
        match = self.build_policy_match(
            rule.source.name, rule.destination.name, app_names)
        then = self.build_policy_then(rule.action)

        if is_global:
            match["from-zone"] = from_zones if from_zones else ["any"]
            match["to-zone"] = to_zones if to_zones else ["any"]
        else:
            ctx = f"{from_zones[0]}_{to_zones[0]}"
            seq = len(self.zonal_policies[ctx]) + 1

        policy_object = {
            "name": f"{ctx}_{seq}",
            "description": rule.name,
            "match": match,
            "then": then
        }

        if is_global:
            self.global_policies.append(policy_object)
        else:
            self.zonal_policies[from_zones[0]
                                ][to_zones[0]].append(policy_object)

    def _build_artifacts(self):
        zonal_policy_objects = []

        for from_zone, to_zones in self.zonal_policies.items():
            for to_zone, policies in to_zones.items():
                zonal_policy_objects.append({
                    "from-zone-name": from_zone,
                    "to-zone-name": to_zone,
                    "policy": policies
                })

        artifact = {
            "applications": {
                "application": self.application_objects
            },
            "security": {
                "address-book": [
                    {
                        "name": "global",
                        "address": self.address_objects,
                        "address-set": self.address_set_objects
                    }
                ],
                "policies": {
                    "policy": zonal_policy_objects
                }
            }
        }

        if self.global_policies:
            artifact["security"]["policies"]["global"] = {
                "policy": self.global_policies
            }

        if not artifact["applications"]["application"]:
            # Workaround bug in Junos for handling empty applications in JSON
            # format
            del artifact["applications"]

        if "apply-group" in self.config:
            applygrp = deepcopy(artifact)
            applygrp["name"] = str(self.config["apply-group"])
            artifact = {"groups": [applygrp]}

        return json.dumps({"configuration": artifact}, indent=4)
