from dataclasses import dataclass
from typing import List

from ...junos_command_builder import JunosCommandBuilder
from .....helpers import default


@dataclass
class JunosSrxAddressSet:
    name: str
    address_names: List[str] = default(list)

    def get_json_config_element(self):
        return {
            "name": self.name,
            "address": [{"name": name} for name in self.address_names]
        }

    def get_set_commands(self, apply_group=None) -> List[str]:
        cmds = JunosCommandBuilder(apply_group)

        config_root = f"security address-book global address-set {self.name}"

        for address_name in self.address_names:
            cmds.add(f"{config_root} address {address_name}")

        return cmds.items
