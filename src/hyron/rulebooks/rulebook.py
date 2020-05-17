from copy import deepcopy
from dataclasses import dataclass
from typing import Dict
from ..helpers import default
from ..apps import ApplicationLibrary
from ..prefixlists import PrefixListLoader
from ..rules import Rule, RuleSet
from ..renderers import Renderer
from ..artifacts import Artifact, ArtifactBlueprint
from ..constants import DEF_ENCODING


@dataclass
class Rulebook:
    title: str = "A Hyron Rulebook"
    owner: str = "Nobody"
    encoding: str = DEF_ENCODING
    apps: ApplicationLibrary = default(ApplicationLibrary)
    prefixlists: PrefixListLoader = default(PrefixListLoader)
    rules: Dict[str, Rule] = default(dict)
    rulesets: Dict[str, RuleSet] = default(dict)
    artifacts: Dict[str, ArtifactBlueprint] = default(dict)
    import_builtins: bool = True

    def build_artifact(self, name: str) -> Artifact:
        blueprint = self.artifacts[name]
        artifact = Artifact(self.encoding)
        artifact.meta = deepcopy(blueprint.meta)
        artifact.meta["_rulebook_title"] = self.title
        artifact.meta["_rulebook_owner"] = self.owner
        artifact.meta["_artifact_name"] = blueprint.name

        for name, filebp in blueprint.files.items():
            renderer = Renderer.get(filebp.renderer, **filebp.config)
            artifact_file = artifact[name]
            data = renderer.build(self.rulesets[filebp.ruleset])

            if renderer.BINARY:
                artifact_file.write_bytes(data)
            else:
                artifact_file.write_text(data)

        return artifact

    def build_all(self):
        return {name: self.build_artifact(name)
                for name in self.artifacts.keys()}
