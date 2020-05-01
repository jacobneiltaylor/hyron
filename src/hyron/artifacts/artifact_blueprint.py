from copy import deepcopy
from typing import Dict
from dataclasses import dataclass
from .artifact import Artifact
from .artifact_file_blueprint import ArtifactFileBlueprint
from ..constants import DEF_ENCODING
from ..helpers import get_plural_dict_item, default

@dataclass
class ArtifactBlueprint:
    name: str
    meta: Dict[str, str]
    files: Dict[str, ArtifactFileBlueprint]

    @classmethod
    def create(cls, name, config):
        files = {k: ArtifactFileBlueprint(k, **v) for k, v in config["files"].items()}
        return cls(name, config["meta"], files)
