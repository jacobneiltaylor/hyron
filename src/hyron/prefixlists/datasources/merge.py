from functools import reduce

from ..prefix_list_loader import PrefixListLoader
from ..prefix_list_datasource import PrefixListDatasource


class MergePrefixListDatasource(PrefixListDatasource, register="merge"):
    def __init__(self, names, loader: PrefixListLoader):
        self._names = names
        self._loader = loader

    def fetch(self):
        prefix_lists = [self._loader[name] for name in self._names]
        return reduce(lambda x, y: x + list(y.prefixes), prefix_lists, [])
