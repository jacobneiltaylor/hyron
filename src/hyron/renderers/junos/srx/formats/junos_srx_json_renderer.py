import json
from ..junos_srx_renderer import JunosSrxRenderer


class JunosSrxJsonRenderer(JunosSrxRenderer, register="jsrx"):
    @staticmethod
    def build_json_data(datastructures):
        return [x.get_json_config_element() for x in datastructures]

    def _build_artifact(self):
        zonal_policy_objects = []

        for from_zone, to_zone in self.get_sorted_zone_pairs():
            policies = self.zonal_policies[from_zone][to_zone]
            zonal_policy_objects.append({
                "from-zone-name": from_zone,
                "to-zone-name": to_zone,
                "policy": self.build_json_data(policies)
            })

        apps, addresses, address_sets = self.get_sorted_objects()

        artifact = {
            "applications": {
                "application": self.build_json_data(apps)
            },
            "security": {
                "address-book": [
                    {
                        "name": "global",
                        "address": self.build_json_data(addresses),
                        "address-set": self.build_json_data(address_sets)
                    }
                ],
                "policies": {
                    "policy": zonal_policy_objects
                }
            }
        }

        if self.global_policies:
            artifact["security"]["policies"]["global"] = {
                "policy": self.build_json_data(self.global_policies)
            }

        # Workaround bug in Junos for handling empty lists in JSON format
        if not artifact["applications"]["application"]:
            del artifact["applications"]

        if not artifact["security"]["policies"]["policy"]:
            del artifact["security"]["policies"]["policy"]

        if "apply-group" in self.config:
            applygrp = {"name": str(self.config["apply-group"])}
            applygrp.update(artifact)
            artifact = {"groups": [applygrp]}

        return json.dumps({"configuration": artifact}, indent=4)
