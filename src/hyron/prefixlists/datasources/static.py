from ..prefix_list_datasource import PrefixListDatasource


class StaticPrefixListDatasource(PrefixListDatasource, register="static"):
    def __init__(self, items):
        self._items = items

    def fetch(self):
        return self._items
