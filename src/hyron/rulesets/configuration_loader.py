import os.path as path
from typing import List
from .rule_builder import RuleBuilder, RuleSetBuilder
from .configuration import Configuration
from ..apps import ApplicationLibraryLoader
from ..helpers import load_yaml, get_builtin_filename, get_base_dir, get_plural_dict_item
from ..renderers import Renderer


class ConfigurationLoadError(RuntimeError):
    """
        Represents an error encountered during processing a config tree
    """
    pass


class ConfigurationLoader():
    def __init__(self):
        self._appldr = ApplicationLibraryLoader()
        self._config = Configuration()
        self._import_builtins = True
        self._meta_read = False
        self._renderer_read = False
        self._meta_filename = ""
        self._current_filename = ""
        self._loaded_filenames = []
        self._renderers = []
        self._rule_builder = RuleBuilder()
        self._rule_set_builder = RuleSetBuilder()

    def _get_include_handler(self, object_type):
        return {
            "appdefs": self._include_app_config,
            "prefixlists": self._include_pfxlst_config
        }[object_type]

    def _clean(self):
        self._config = Configuration()
        self._import_builtins = True
        self._meta_read = False
        self._renderer_read = False
        self._meta_filename = ""
        self._current_filename = ""
        self._loaded_filenames = []
        self._renderers = []

    def _load_yaml(self, filename: str) -> dict:
        self._current_filename = filename
        self._loaded_filenames.append(filename)
        return load_yaml(filename)

    def _get_builtin_data(self, name):
        return self._load_yaml(get_builtin_filename(name))

    def _include_app_config(self, appdata):
        self._appldr.load(appdata, self._config.apps)

    def _include_pfxlst_config(self, pfxlstdata):
        self._config.prefixlists.include(pfxlstdata)

    def _load_builtins(self):
        self._include_app_config(self._get_builtin_data("apps")["objects"]["appdefs"])
        self._include_pfxlst_config(self._get_builtin_data("prefixlists")["objects"]["prefixlists"])

    def _process_configuration_data(self, confdata: dict):
         for stanza, stanzadata in confdata.items():
             if hasattr(self, stanza):
                getattr(self, stanza)(stanzadata)

    def _process_rules(self):
        self._rule_builder.resolve(self._config)
        self._rule_set_builder.resolve(self._config)

    def _process_renderers(self):
        for renderer, rulesets in self._renderers:
            for name in rulesets:
                renderer.queue_job(name, self._config.rulesets[name])
            self._config.renderers.append(renderer)

    def load(self, filename: str) -> Configuration:
        self._clean()
        self._config.title = filename

        self._process_configuration_data(self._load_yaml(filename))

        if self._import_builtins:
            self._load_builtins()

        self._process_rules()
        self._process_renderers()

        return self._config

    def meta(self, stanzadata: dict):
        if not self._meta_read:
            self._meta_read = True
            
            if "title" in stanzadata:
                self._config.title = stanzadata["title"]

            self._import_builtins = stanzadata.get("import_builtins", True)
            self._config.owner = stanzadata.get("owner", "Nobody")
        else:
            raise ConfigurationLoadError("Multiple metadata stanzas detected in config tree!")
            
    def objects(self, stanzadata: dict):
        for object_type, config in stanzadata.items():
            self._get_include_handler(object_type)(config)

    def imports(self, stanzadata: List[str]):
        for import_file in stanzadata:
            filepath = import_file.split(".")
            base_dir = get_base_dir(self._current_filename)
            filename = f"{path.join(base_dir, *filepath)}.yaml"
            temp = self._current_filename
            self._process_configuration_data(self._load_yaml(filename))
            self._current_filename = temp

    def rules(self, stanzadata: dict):
        for name, rule_config in stanzadata.items():
            self._rule_builder.add(name, rule_config)
    
    def rulesets(self, stanzadata: dict):
        for name, ruleset_configs in stanzadata.items():
            self._rule_set_builder.add(name, ruleset_configs)
    
    def renderers(self, stanzadata: dict):
        if not self._renderer_read:
            self._renderer_read = True
            for name, renderer_config in stanzadata.items():
                ruleset_names = get_plural_dict_item(renderer_config, "ruleset")
                config = renderer_config.get("config", {})
                self._renderers.append((Renderer.get(name, **config), ruleset_names))
        else:
            raise ConfigurationLoadError("Multiple renderer stanzas detected in config tree!")