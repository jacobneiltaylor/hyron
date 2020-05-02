from plugable import Plugable


class PrefixListDatasource(Plugable):
    def fetch(self):
        raise NotImplementedError()
