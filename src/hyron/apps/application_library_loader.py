from .application import Application, PortApplication
from .application_library import ApplicationLibrary


_FROMPORT = "from-port"
_TOPORT = "to-port"
_PORT = "port"
_PORT_PROTOCOLS = {
    Application.TCP,
    Application.UDP
}


class ApplicationLibraryLoader:
    @staticmethod
    def _resolve_protocol(appdef):
        protocol = appdef["protocol"]
        if isinstance(protocol, int):
            return protocol
        else:
            protocol = protocol.upper()
            if hasattr(Application, protocol):
                return getattr(Application, protocol)
            else:
                raise NotImplementedError(f"{protocol} is not implemented")

    @staticmethod
    def _resolve_ports(appdef):
        if _FROMPORT in appdef and _TOPORT in appdef:
            return (appdef[_FROMPORT], appdef[_TOPORT])
        return (appdef[_PORT], appdef[_PORT])

    def _load_apps(self, appdefs: dict, lib):
        for name, appdef in appdefs.items():
            protocol = self._resolve_protocol(appdef)

            if protocol in _PORT_PROTOCOLS:
                ports = self._resolve_ports(appdef)
                app = PortApplication(protocol, *ports)
            else:
                app = Application(protocol)

            app.metadata.update(appdef.get("meta", {}))
            lib.register_app(name, app)

    def _load_appgroups(self, appgroupdefs: dict, lib):
        for name, applist in appgroupdefs.items():
            lib.build_appgroup(name, applist)

    def load(self, config: dict, lib: ApplicationLibrary = None):
        if not lib:
            lib = ApplicationLibrary()
        self._load_apps(config["apps"], lib)
        self._load_appgroups(config["appgroups"], lib)
        return lib
