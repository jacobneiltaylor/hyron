from ipaddress import ip_network
from dataclasses import dataclass
from typing import List

from ...junos_command_builder import JunosCommandBuilder


@dataclass
class JunosSrxAddress:
    name: str
    address: str

    @classmethod
    def get_for_prefix(cls, prefix: str, existing: dict):
        net = ip_network(prefix)
        network_addr = net.network_address.compressed
        name = f"pfx{net.version}-{network_addr}-{net.prefixlen}"

        if name not in existing:
            existing[name] = cls(name, net.exploded)

        return existing[name]

    def get_json_config_element(self):
        return {
            "name": self.name,
            "ip-prefix": self.address
        }

    def get_set_commands(self, apply_group=None) -> List[str]:
        cmds = JunosCommandBuilder(apply_group)

        cmds.add(f"security address-book global address {self.name} {self.address}")  # noqa

        return cmds.items
