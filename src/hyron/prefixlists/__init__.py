from .prefix_list import PrefixList
from .prefix_list_loader import PrefixListLoader
from .prefix_list_datasource import PrefixListDatasource
from . import datasources

from ..helpers import load_yaml, get_builtin_filename


_BUILTINS = "prefixlists"


def get_builtin_prefixlists():
    return PrefixListLoader(load_yaml(get_builtin_filename(_BUILTINS))[_BUILTINS])


__all__ = [
    "PrefixList",
    "PrefixListLoader",
    "PrefixListDatasource",
    "get_builtin_prefixlists",
    "datasources"
]