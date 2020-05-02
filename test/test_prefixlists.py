import hyron
import testconstants


def _get_builtin_prefixlist_config():
    return hyron.helpers.load_yaml(
        hyron.helpers.get_builtin_filename("prefixlists"))


def _get_prefixlist_loader():
    prefix_list_config = _get_builtin_prefixlist_config()
    prefix_list_config["objects"]["prefixlists"]["dummy"] = {
        "type": "__nonexist__"
    }
    return hyron.prefixlists.PrefixListLoader(
        prefix_list_config["objects"]["prefixlists"])


def test_prefixlists():
    prefixlists = _get_prefixlist_loader()
    expected = len(_get_builtin_prefixlist_config()["objects"]["prefixlists"])

    assert(len(prefixlists.available) == expected)
    assert(len(prefixlists.loaded) == 0)

    for name, assertions in testconstants.PREFIX_LIST_TESTS.items():
        prefixlist = prefixlists[name]

        if "contains" in assertions:
            for prefix in assertions["contains"]:
                assert(prefix in prefixlist)
        if "not" in assertions:
            for prefix in assertions["not"]:
                assert(prefix not in prefixlist)

    # Merge providers will trigger loading of
    # other providers, therefore >= is used here
    assert(len(prefixlists.loaded) >= len(testconstants.PREFIX_LIST_TESTS))
