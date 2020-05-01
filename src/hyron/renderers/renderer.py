from abc import abstractmethod
from typing import Dict
from plugable import Plugable
from ..rules.rule_set import RuleSet, Rule
from ..apps.application import Application
from ..prefixlists.prefix_list import PrefixList
from ..helpers import on_dict_match


class Renderer(Plugable):
    """
        Renderers take compiled rule-set objects and output one or more
        "artifacts", which are a text-based representation of rules in a
        format native to a device or system capable of enforcing them.
    """
    BINARY = False  # Set this flag to true if your Renderer outputs binary

    def __init__(self, **config):
        self.config = config
        self.metadata = None
        self.preprocess_entities = False

    def build(self, rule_set: RuleSet) -> Dict[str, str]:
        self.metadata = rule_set.metadata

        self._initialise()

        if self.preprocess_entities:
            for pfx_list in rule_set.prefix_lists:
                self._preprocess_prefix_list(pfx_list)
            for app in rule_set.applications:
                self._preprocess_app(app)

        for rule in rule_set.rules:
            self._process_rule(rule)

        return self._build_artifacts()

    def _assert_metadata(self, key, value, if_retval, else_retval):
        return on_dict_match(self.metadata, key, value, if_retval, else_retval)

    def _initialise(self):
        return

    def _preprocess_prefix_list(self, prefixes: PrefixList):
        raise NotImplementedError

    def _preprocess_app(self, app: Application):
        raise NotImplementedError

    @abstractmethod
    def _process_rule(self, rule: Rule):
        pass

    @abstractmethod
    def _build_artifacts(self):
        pass
