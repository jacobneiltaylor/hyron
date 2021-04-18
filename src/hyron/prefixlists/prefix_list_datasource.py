from plugable import Plugable


class PrefixListDatasource(Plugable):
    """
        Represents a datasource for prefix lists
    """
    def fetch(self):
        raise NotImplementedError()
