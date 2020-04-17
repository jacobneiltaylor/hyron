from dataclasses import dataclass, field
from typing import List, Dict
from ..apps import ApplicationLibrary
from ..prefixlists import PrefixListLoader
from ..rules import Rule, RuleSet
from ..renderers import Renderer

@dataclass
class Configuration:
    title: str = ""
    owner: str = ""
    apps: ApplicationLibrary = field(default_factory=lambda: ApplicationLibrary())
    prefixlists: PrefixListLoader = field(default_factory=lambda: PrefixListLoader())
    rules: Dict[str,Rule] = field(default_factory=dict)
    rulesets: Dict[str,RuleSet] = field(default_factory=dict)
    renderers: List[Renderer] = field(default_factory=list)
