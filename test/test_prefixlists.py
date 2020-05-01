import hyron
import testconstants


def _get_prefixlist_loader():
    prefix_list_config = hyron.helpers.load_yaml(
        hyron.helpers.get_builtin_filename("prefixlists"))
    return hyron.prefixlists.PrefixListLoader(
        prefix_list_config["objects"]["prefixlists"])


def test_prefixlists():
    prefixlists = _get_prefixlist_loader()

    for name, assertions in testconstants.PREFIX_LIST_TESTS.items():
        prefixlist = prefixlists[name]

        if "contains" in assertions:
            for prefix in assertions["contains"]:
                assert(prefix in prefixlist)
        if "not" in assertions:
            for prefix in assertions["not"]:
                assert(prefix not in prefixlist)
