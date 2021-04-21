class JunosCommandBuilder:
    def __init__(self, apply_group=None):
        self.apply_group = apply_group
        self.items = []

    @property
    def set_prefix(self):
        if self.apply_group is not None:
            return f"set groups {self.apply_group}"
        return "set"

    def add(self, cmd, no_append=False, front=False):
        if not no_append:
            cmd = f"{self.set_prefix} {cmd}"

        if front:
            self.items.insert(0, cmd)
        else:
            self.items.append(cmd)
