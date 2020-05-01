from abc import ABC, abstractproperty
from typing import List
from ..constants import PROTOCOLS


class ApplicationContainer(ABC):
    @abstractproperty
    def apps(self) -> List["Application"]:
        pass

    @abstractproperty
    def name(self) -> str:
        pass

    @abstractproperty
    def deterministic_name(self) -> str:
        pass

    def __hash__(self):
        return hash(self.deterministic_name)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.deterministic_name} at {hex(id(self))}>"  # noqa

    def __eq__(self, other):
        return self._unique_name == other._unique_name

    @property
    def _unique_name(self):
        if self.name != self.deterministic_name:
            return f"{self.name}({self.deterministic_name})"
        return self.deterministic_name


class Application(ApplicationContainer):
    ICMP = 1
    ICMPV6 = 53
    TUNIP4 = 4
    TCP = 6
    UDP = 17
    TUNIP6 = 41
    GRE = 47
    SCTP = 132

    def __init__(self, protocol: int):
        self._protocol = protocol
        self.metadata = {}

    def __le__(self, app):
        return self._protocol == app._protocol

    @property
    def apps(self):
        return [self]

    @property
    def name(self):
        if "name" in self.metadata:
            return self.metadata["name"]
        return self.deterministic_name

    @property
    def protocol(self):
        if self._protocol in PROTOCOLS:
            return PROTOCOLS[self._protocol].lower()
        return str(self._protocol)

    @property
    def protocol_id(self):
        return self._protocol

    @property
    def deterministic_name(self):
        return f"protocol_{self.protocol}"


class PortApplication(Application):
    def __init__(self, protocol: int, from_port: int, to_port: int):
        self.from_port = from_port
        self.to_port = to_port
        super().__init__(protocol)

    def __contains__(self, port):
        return self.from_port <= port <= self.to_port

    def __le__(self, app):
        if isinstance(app, type(self)):
            return self.protocol == app.protocol and self.to_port in app and self.from_port in app  # noqa
        return False

    @classmethod
    def tcp_port(cls, port):
        return cls(cls.TCP, port, port)

    @classmethod
    def tcp_port_range(cls, from_port, to_port):
        return cls(cls.TCP, from_port, to_port)

    @classmethod
    def udp_port(cls, port):
        return cls(cls.UDP, port, port)

    @classmethod
    def udp_port_range(cls, from_port, to_port):
        return cls(cls.UDP, from_port, to_port)

    @property
    def name(self):
        if "name" in self.metadata:
            return self.metadata["name"]
        elif self.from_port == self.to_port:
            return f"{super().name}_port_{self.from_port}"
        return f"{super().name}_ports_{self.from_port}_to_{self.to_port}"

    @property
    def deterministic_name(self):
        if self.from_port == self.to_port:
            return f"{super().deterministic_name}_port_{self.from_port}"
        return f"{super().deterministic_name}_ports_{self.from_port}_to_{self.to_port}"  # noqa
