import os
import radix

from ruamel import yaml


def get_base_dir(filename):
    return os.path.dirname(os.path.realpath(filename))


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
    with open(filename, 'r') as infile:
        return yaml.load(infile, yaml.Loader)


def get_builtin_filename(name):
    return os.path.join(get_base_dir(__file__), "builtin", f"{name}.yaml")


def on_dict_match(dic, key, value, if_retval, else_retval):
        if key in dic and dic[key] == value:
            return if_retval
        return else_retval
