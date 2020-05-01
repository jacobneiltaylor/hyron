import os
from dataclasses import field
import radix

from ruamel import yaml


def _load(filename, handler):
    with open(filename, 'r') as infile:
        return handler(infile)


def _get_pkg_filename(*args):
    return os.path.join(get_pkg_dir(), *args)


def default(factory):
    return field(default_factory=factory)


def get_base_dir(filename):
    return os.path.dirname(os.path.realpath(filename))


def get_pkg_dir():
    return get_base_dir(__file__)


def optimise_prefixes(*prefix_list):
    rt = radix.Radix()

    for prefix in prefix_list:
        rt.add(prefix)

    return set([rt.search_worst(prefix).prefix for prefix in prefix_list])


def as_list(item):
    if isinstance(item, list):
        return item
    return [item]


def get_plural_dict_item(dic, name, single_handler=lambda x: [x]):
    plural = f"{name}s"
    if name in dic:
        return single_handler(dic[name])
    elif plural in dic:
        return dic[plural]
    raise KeyError(name)


def load_yaml(filename):
    return _load(filename, lambda x: yaml.load(x, yaml.Loader))


def load_text(filename):
    return _load(filename, lambda x: x.read())


def get_builtin_filename(name):
    return _get_pkg_filename("builtin", f"{name}.yaml")


def get_asset_filename(name, ext="txt"):
    return _get_pkg_filename("assets", f"{name}.{ext}")


def on_dict_match(dic, key, value, if_retval, else_retval):
    if key in dic and dic[key] == value:
        return if_retval
    return else_retval
