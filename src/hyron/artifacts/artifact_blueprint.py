from typing import Dict
from dataclasses import dataclass
from .artifact_file_blueprint import ArtifactFileBlueprint


@dataclass
class ArtifactBlueprint:
    name: str
    meta: Dict[str, str]
    files: Dict[str, ArtifactFileBlueprint]

    @classmethod
    def create(cls, name, config):
        files = {k: ArtifactFileBlueprint(k, **v)
                 for k, v in config["files"].items()}
        return cls(name, config["meta"], files)
