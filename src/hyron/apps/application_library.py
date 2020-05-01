
from .application import Application
from .application_group import ApplicationGroup


class ApplicationLibrary:
    def __init__(self):
        self._apps = {}
        self._appgroups = {}

    def register_app(self, name: str, app: Application):
        app.metadata["name"] = name
        self._apps[name] = app

    def register_appgroup(self, name: str, appgroup: ApplicationGroup):
        appgroup.metadata["name"] = name
        self._appgroups[name] = appgroup

    @property
    def apps(self):
        return set(self._apps.keys())

    @property
    def appgroups(self):
        return set(self._appgroups.keys())

    def __getitem__(self, item):
        if item in self._apps:
            return self._apps[item]
        elif item in self._appgroups:
            return self._appgroups[item]
        raise KeyError(item)

    def build_appgroup(self, name: str, members: list):
        apps = []
        for member in members:
            apps += self[member].apps
        appgroup = ApplicationGroup(apps)
        self.register_appgroup(name, appgroup)
