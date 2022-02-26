from functools import reduce
from typing import Iterable

from ..junos_srx_renderer import JunosSrxRenderer
from ..datastructures import JunosSrxDatastructure


class JunosSrxCommandRenderer(JunosSrxRenderer, register="jsrx-cmd"):
    @staticmethod
    def flatten(lists):
        return reduce(lambda x, y: x + y, lists, [])

    @classmethod
    def build_commands(cls, datastructures: Iterable[JunosSrxDatastructure], apply_group=None):  # noqa
        return cls.flatten(
            map(lambda x: x.get_set_commands(apply_group), datastructures)
        )

    def _build_artifact(self):
        commands = []
        apply_group = None

        if "apply-group" in self.config:
            apply_group = str(self.config["apply-group"])
            commands.append(f"delete groups {apply_group}")
        else:
            commands = [
                "delete security policies",
                "delete security address-book global",
                "delete applications"
            ]

        apps, addresses, address_sets = self.get_sorted_objects()

        commands += self.build_commands(addresses, apply_group)
        commands += self.build_commands(address_sets, apply_group)
        commands += self.build_commands(apps, apply_group)
        commands += self.build_commands(self.global_policies, apply_group)

        for from_zone, to_zone in self.get_sorted_zone_pairs():
            policies = self.zonal_policies[from_zone][to_zone]
            commands += self.build_commands(policies, apply_group)

        if apply_group:
            commands.append(f"set apply-groups {apply_group}")

        return "\n".join(commands)
