from .configuration import Configuration
from ..rules import Rule, RuleSet
from ..apps import ApplicationLibrary
from ..prefixlists import PrefixList, PrefixListLoader, get_builtin_prefixlists
from ..constants import ACTION_PERMIT, ACTIONS

_DEF_PFX = PrefixList(["0.0.0.0/0", "::/0"], name="any")

class RuleBuilder:
    def __init__(self):
        self._proto_rules = {}

    def add(self, name: str, rule_config: dict):
        src = rule_config.get("src", None)
        dst = rule_config.get("dst", None)
        action = rule_config.get("action", ACTION_PERMIT)
        meta = rule_config.get("meta", {})
        app = rule_config["app"]

        assert(action in ACTIONS)
        
        self._proto_rules[name] = (src, dst, app, action, meta)

    def resolve(self, config: Configuration):
        rules = {}

        for name, (src, dst, app, action, meta) in self._proto_rules.items():
            src_pfxs = _DEF_PFX
            dst_pfxs = _DEF_PFX

            if src:
                src_pfxs = config.prefixlists[src]

            if dst:
                dst_pfxs = config.prefixlists[dst]

            rules[name] = Rule(src_pfxs, dst_pfxs, config.apps[app], action, name=name, **meta)
        
        self._proto_rules = {}
        config.rules.update(rules)

class RuleSetBuilder:
    def __init__(self):
        self._proto_rule_sets = {}

    def add(self, name: str, ruleset_config: dict):
        self._proto_rule_sets[name] = (ruleset_config["rules"], ruleset_config.get("meta", {}))

    def resolve(self, config: Configuration):
        rule_sets = {
            setname: RuleSet([config.rules[name] for name in rulenames], **meta) 
            for setname, (rulenames, meta) in self._proto_rule_sets.items()
        }
            
        self._proto_rule_sets = {}
        config.rulesets.update(rule_sets)