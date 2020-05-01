from metaloader import FlatLoader, YamlSerialisation, LoaderContext
from .rule_builder import RuleBuilder, RuleSetBuilder
from .rulebook import Rulebook
from ..apps import ApplicationLibraryLoader
from ..artifacts import ArtifactBlueprint
from ..helpers import get_builtin_filename, load_yaml
from ..constants import LOADER_SCHEMA


class RulebookLoader:
    def __init__(self, fs=None):
        self._cfgldr = FlatLoader(YamlSerialisation())
        self._cfgldr.set_schema(LOADER_SCHEMA)
        self._appldr = ApplicationLibraryLoader()
        self._builtins = {}
        self.last_ctx: LoaderContext = None
        self.fs = fs

        self._load_builtin("apps")
        self._load_builtin("prefixlists")

    def _load_builtin(self, name):
        filename = get_builtin_filename(name)
        self._builtins[name] = load_yaml(filename)

    @staticmethod
    def _load_metadata(metadata: dict, rulebook: Rulebook):
        for key in ("title", "encoding", "import_builtins", "owner"):
            if key in metadata:
                setattr(rulebook, key, metadata[key])

    @staticmethod
    def _include_pfxlst_config(pfxlsts, rulebook: Rulebook):
        rulebook.prefixlists.include(pfxlsts)

    @staticmethod
    def _prepare_dict(objects, keys):
        for key in keys:
            if key not in objects:
                objects[key] = {}

    def _include_app_config(self, apps, rulebook: Rulebook):
        self._appldr.load(apps, rulebook.apps)

    def _get_include_handler(self, object_type):
        return {
            "appdefs": self._include_app_config,
            "prefixlists": self._include_pfxlst_config
        }[object_type]

    def _load_objects(self, objects: dict, rulebook: Rulebook):
        def apps(dct):
            return dct["appdefs"]["apps"]

        def appgroups(dct):
            return dct["appdefs"]["appgroups"]

        self._prepare_dict(objects, ["appdefs", "prefixlists"])
        self._prepare_dict(objects["appdefs"], ["apps", "appgroups"])

        if rulebook.import_builtins:
            apps(objects).update(apps(self._builtins["apps"]["objects"]))
            appgroups(objects).update(
                appgroups(self._builtins["apps"]["objects"]))
            objects["prefixlists"].update(
                self._builtins["prefixlists"]["objects"]["prefixlists"])

        for name, config in objects.items():
            self._get_include_handler(name)(config, rulebook)

    @staticmethod
    def _load_rules(rules: dict, rulebook: Rulebook):
        builder = RuleBuilder()
        for name, rule in rules.items():
            builder.add(name, rule)
        builder.resolve(rulebook)

    @staticmethod
    def _load_rulesets(rulesets: dict, rulebook: Rulebook):
        builder = RuleSetBuilder()
        for name, ruleset in rulesets.items():
            builder.add(name, ruleset)
        builder.resolve(rulebook)

    @staticmethod
    def _load_artifacts(artifacts: dict, rulebook: Rulebook):
        for name, config in artifacts.items():
            rulebook.artifacts[name] = ArtifactBlueprint.create(name, config)

    def load(self, filename: str) -> Rulebook:
        rulebook = Rulebook()
        rulebook.title = filename

        ctx = self._cfgldr.load(filename, self.fs)

        self._load_metadata(ctx.data["meta"], rulebook)
        self._load_objects(ctx.data["objects"], rulebook)
        self._load_rules(ctx.data["rules"], rulebook)
        self._load_rulesets(ctx.data["rulesets"], rulebook)
        self._load_artifacts(ctx.data["artifacts"], rulebook)

        self.last_ctx = ctx

        return rulebook
