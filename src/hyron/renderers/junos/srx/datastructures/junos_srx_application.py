from dataclasses import dataclass
from typing import Optional, List

from ...junos_command_builder import JunosCommandBuilder
from .....apps import Application, PortApplication


@dataclass
class JunosSrxApplication:
    name: str
    protocol: str
    from_port: Optional[str] = None
    to_port: Optional[str] = None

    @classmethod
    def from_app(cls, app: Application):
        this = cls(app.name, app.protocol)

        if isinstance(app, PortApplication):
            this.from_port = app.from_port
            this.to_port = app.to_port

        return this

    @property
    def destination_port_content(self):
        if self.from_port:
            dstport = self.from_port
            if self.to_port and self.to_port != dstport:
                dstport = f"{dstport}-{self.to_port}"
            return dstport
        return None

    def get_json_config_element(self):
        element = {
            "name": self.name,
            "protocol": self.protocol,
        }

        dstport = self.destination_port_content

        if dstport:
            element["destination-port"] = dstport

        return element

    def get_set_commands(self, apply_group=None) -> List[str]:
        cmds = JunosCommandBuilder(apply_group)
        config_root = f"applications application {self.name}"
        dstport = self.destination_port_content

        cmds.add(f"{config_root} protocol {self.protocol}")
        if dstport:
            cmds.add(f"{config_root} destination-port {dstport}")

        return cmds.items
