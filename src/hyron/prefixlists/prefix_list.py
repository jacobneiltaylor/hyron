import ipaddress
from collections import defaultdict

import radix

from ..helpers import optimise_prefixes

def _explode(nets: list):
    return list(map(lambda x: x.exploded, nets))

class PrefixList:
    NAME_PREFIX = "nets"

    def __init__(self, prefixes, **meta):
        self._prefixes = optimise_prefixes(*prefixes)
        self._ipv4_prefixes = []
        self._ipv6_prefixes = []
        self._reorder_prefixes()

        self._radix = radix.Radix()
        for prefix in self._prefixes:
            self._radix.add(prefix)
        self.metadata = meta
        self._repr = self._calculate_repr()

    def _calculate_repr(self):
        joined_pfxs = ",".join(self.prefixes)
        return f"{self.name}({joined_pfxs})"

    def __repr__(self):
        return self._repr

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __contains__(self, prefix):
        if self.search(prefix):
            return True
        return False

    @property
    def prefixes(self):
        return self._prefixes

    def _reorder_prefixes(self):
        nets = defaultdict(lambda: [])

        for ip_network in map(ipaddress.ip_network, self._prefixes):
            nets[ip_network.version].append(ip_network)

        for net_list in nets.values():
            net_list.sort()

        self._ipv4_prefixes = _explode(nets[4])
        self._ipv6_prefixes = _explode(nets[6])

        self._prefixes = self._ipv4_prefixes + self._ipv6_prefixes

    @property
    def ipv4_prefixes(self):
        return self._ipv4_prefixes

    @property
    def ipv6_prefixes(self):
        return self._ipv6_prefixes

    def search(self, prefix):
        result = self._radix.search_best(prefix)
        if result:
            result = result.prefix
        return result

    @property
    def name(self):
        name = self.metadata["name"]
        return f"{self.NAME_PREFIX}_{name}"


class Host(PrefixList):
    NAME_PREFIX = "host"

    def __init__(self, ipv4addr: str = None, ipv6addr: str = None, **meta):
        self.ipv4addr = ipv4addr
        self.ipv6addr = ipv6addr

        prefixes = []

        if ipv4addr:
            prefixes.append(ipv4addr)

        if ipv6addr:
            prefixes.append(ipv6addr)

        super().__init__(prefixes, **meta)


class HostList(PrefixList):
    NAME_PREFIX = "hosts"

    def __init__(self, hosts=[], **meta):
        super().__init__([host.prefixes for host in hosts], **meta)
