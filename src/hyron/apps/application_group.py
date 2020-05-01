from .application import ApplicationContainer


class ApplicationGroup(ApplicationContainer):
    def __init__(self, apps=[]):
        self._apps = apps
        self.metadata = {}

    @property
    def apps(self):
        return self._apps

    @property
    def name(self):
        if "name" in self.metadata:
            return self.metadata["name"]
        return self.deterministic_name

    @property
    def deterministic_name(self):
        joined_apps = ",".join(map(lambda x: x.deterministic_name, self.apps))
        return f"group({joined_apps})"

    # TODO: Add application group optimisation logic, deterministic sorting
