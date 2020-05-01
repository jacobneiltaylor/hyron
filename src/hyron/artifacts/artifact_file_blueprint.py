from typing import Dict
from dataclasses import dataclass


@dataclass
class ArtifactFileBlueprint:
    name: str
    renderer: str
    ruleset: str
    config: Dict[str, str]
