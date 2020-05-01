from copy import deepcopy
from base64 import b64encode, b64decode
from .artifact_file import ArtifactFile
from ..constants import DEF_ENCODING


class Artifact:
    def __init__(self, encoding=DEF_ENCODING):
        self.encoding = encoding
        self.meta = {}
        self.files = {}

    def __getitem__(self, key) -> ArtifactFile:
        if key not in self.files:
            self.files[key] = ArtifactFile(key, self.encoding)
        return self.files[key]

    def close_all(self):
        for file_obj in self.files.values():
            file_obj.close()

    def to_manifest(self):
        def encode(file_obj: ArtifactFile):
            return b64encode(file_obj.get_contents()).decode("ascii")

        meta = deepcopy(self.meta)
        meta["_encoding"] = self.encoding

        return {
            "meta": meta,
            "files": {k: encode(v) for k, v in self.files.items()}
        }

    @classmethod
    def from_manifest(cls, manifest: dict) -> "Artifact":
        def decode(data: str):
            return b64decode(data.encode("ascii"))

        artifact = cls(manifest["meta"]["_encoding"])

        for k, v in manifest["files"].items():
            file_obj = artifact[k]
            file_obj.write_bytes(decode(v))

        artifact.close_all()

        return artifact
