from ..prefix_list_datasource import PrefixListDatasource


class StaticPrefixListDatasource(PrefixListDatasource, register="static"):
    """
        This datasource allows users to define static prefix lists
    """
    def __init__(self, items):
        self._items = items

    def fetch(self):
        return self._items
