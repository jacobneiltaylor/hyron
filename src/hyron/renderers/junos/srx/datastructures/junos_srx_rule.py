from dataclasses import dataclass
from typing import List, Optional

from ...junos_command_builder import JunosCommandBuilder


@dataclass
class JunosSrxRule:
    description: str
    source: str
    destination: str
    applications: List[str]
    action: str
    force_global: bool = False
    from_zones: Optional[List[str]] = None
    to_zones: Optional[List[str]] = None
    comment: Optional[str] = None
    name: Optional[str] = None

    @property
    def is_global(self):
        if self.from_zones and self.to_zones and not self.force_global:
            return len(self.from_zones) == 1 and len(self.to_zones) == 1
        return True

    def get_json_config_element(self):
        element = {
            "name": self.name if self.name else self.description,
            "description": self.description,
            "match": {
                "source-address": [self.source],
                "destination-address": [self.destination],
                "application": self.applications
            },
            "then": {
                self.action: [None]
            }
        }

        if self.is_global:
            element["match"]["from-zones"] = self.from_zones
            element["match"]["to-zones"] = self.to_zones

        if self.comment:
            element["@"] = {
                "comment": self.comment
            }

        return element

    def get_set_commands(self, apply_group=None) -> List[str]:
        cmds = JunosCommandBuilder(apply_group)
        name = self.name if self.name else self.description
        config_root = "security policies"

        if self.is_global:
            config_root = f"{config_root} global policy {name}"
            if self.from_zones:
                for from_zone in self.from_zones:
                    cmds.add(f"{config_root} match from-zone {from_zone}")
            if self.to_zones:
                for to_zone in self.from_zones:
                    cmds.add(f"{config_root} match to-zone {to_zone}")
        else:
            from_zone = self.from_zones[0]
            to_zone = self.to_zones[0]
            config_root = f"{config_root} from-zone {from_zone} to-zone {to_zone} policy {name}"  # noqa

        cmds.add(f"{config_root} match source-address {self.source}")
        cmds.add(f"{config_root} match destination-address {self.destination}")

        for app in self.applications:
            cmds.add(f"{config_root} match application {app}")

        cmds.add(f"{config_root} then {self.action}")

        return cmds.items
