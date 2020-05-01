import os
import hyron
import metaloader
import testconstants


def _get_test_rulebook_path(name):
    return os.path.join(
        testconstants.TEST_DIRECTORY,
        "data",
        "rulebooks",
        name,
        "main.yaml")


def _load_rulebook(filename):
    loader = hyron.rulebooks.RulebookLoader()
    return loader.load(filename)


def _load_datastructure(filename):
    loader = metaloader.FlatLoader(
        serialisation=metaloader.YamlSerialisation())
    loader.set_schema(hyron.constants.LOADER_SCHEMA)
    return loader.load(filename).data


def test_integration():
    filename = _get_test_rulebook_path("simple")
    rulebook = _load_rulebook(filename)
    data = _load_datastructure(filename)
    assert(rulebook.title == data["meta"]["title"])
    assert(rulebook.owner == data["meta"]["owner"])
    artifacts = rulebook.build_all()

    for name in data["artifacts"].keys():
        assert(name in artifacts)
