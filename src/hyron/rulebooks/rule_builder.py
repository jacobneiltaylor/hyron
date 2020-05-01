from .rulebook import Rulebook
from ..rules import Rule, RuleSet
from ..prefixlists import PrefixList
from ..constants import ACTION_PERMIT, ACTIONS

_DEF_PFX = PrefixList(["0.0.0.0/0", "::/0"], name="any")


class RuleBuilder:
    def __init__(self):
        self._proto_rules = {}

    def add(self, name: str, rule: dict):
        src = rule.get("src", None)
        dst = rule.get("dst", None)
        action = rule.get("action", ACTION_PERMIT)
        meta = rule.get("meta", {})
        app = rule["app"]

        assert(action in ACTIONS)

        self._proto_rules[name] = (src, dst, app, action, meta)

    def resolve(self, rulebook: Rulebook):
        rules = {}

        for name, (src, dst, app, action, meta) in self._proto_rules.items():
            src_pfxs = _DEF_PFX
            dst_pfxs = _DEF_PFX

            if src:
                src_pfxs = rulebook.prefixlists[src]

            if dst:
                dst_pfxs = rulebook.prefixlists[dst]

            rules[name] = Rule(
                src_pfxs,
                dst_pfxs,
                rulebook.apps[app],
                action,
                name=name,
                **meta)

        self._proto_rules = {}
        rulebook.rules.update(rules)


class RuleSetBuilder:
    def __init__(self):
        self._proto_rule_sets = {}

    def add(self, name: str, ruleset: dict):
        self._proto_rule_sets[name] = (
            ruleset["rules"], ruleset.get("meta", {}))

    def resolve(self, rulebook: Rulebook):
        rule_sets = {
            setname: RuleSet([rulebook.rules[name] for name in rulenames], **meta)  # noqa
            for setname, (rulenames, meta) in self._proto_rule_sets.items()
        }

        self._proto_rule_sets = {}
        rulebook.rulesets.update(rule_sets)
