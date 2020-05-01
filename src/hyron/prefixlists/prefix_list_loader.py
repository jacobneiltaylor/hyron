from copy import copy

from .prefix_list import PrefixList
from .prefix_list_datasource import PrefixListDatasource


class PrefixListLoader:
    def __init__(self, config: dict = None):
        self._datasources = {}
        self._cached = {}
        self._types = PrefixListDatasource.registry.enum()
        if config:
            self.include(config)

    def include(self, config: dict):
        for name, ds_config in config.items():
            ds_type = ds_config["type"]
            if ds_type in self._types:
                kwargs = copy(ds_config)
                del kwargs["type"]
                if ds_type == "merge":
                    # merge pfx lists require access to the loader to reference
                    # other prefix lists
                    kwargs["loader"] = self
                self._datasources[name] = PrefixListDatasource.get(
                    ds_type, **kwargs)

    @property
    def available(self):
        return set(self._datasources.keys())

    @property
    def loaded(self):
        return set(self._cached.keys())

    def __getitem__(self, key) -> PrefixList:
        if key not in self._cached:
            prefixes = self._datasources[key].fetch()
            self._cached[key] = PrefixList(prefixes, name=key)
        return self._cached[key]
