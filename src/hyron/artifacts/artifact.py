import os
import json
import shutil
import tempfile
from copy import deepcopy
from base64 import b64encode, b64decode
from typing import Dict
from .artifact_file import ArtifactFile
from ..constants import DEF_ENCODING
from ..helpers import resolve_working_directory


class Artifact:
    def __init__(self, encoding=DEF_ENCODING):
        self.encoding = encoding
        self.meta = {}
        self.files: Dict[str, ArtifactFile] = {}

    def __getitem__(self, key) -> ArtifactFile:
        if key not in self.files:
            self.files[key] = ArtifactFile(key, self.encoding)
        return self.files[key]

    def close_all(self):
        for file_obj in self.files.values():
            file_obj.close()

    def _get_encodable_meta(self):
        meta = deepcopy(self.meta)
        meta["_encoding"] = self.encoding
        return meta

    def to_manifest(self):
        def encode(file_obj: ArtifactFile):
            return b64encode(file_obj.get_contents()).decode("ascii")

        return {
            "meta": self._get_encodable_meta(),
            "files": {k: encode(v) for k, v in self.files.items()}
        }

    @property
    def name(self):
        return self.meta.get("_artifact_name", "artifact")

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

    def to_json(self) -> str:
        return json.dumps(self.to_manifest())

    def to_file_structure(self, rootdir=None):
        rootdir = resolve_working_directory(rootdir)

        def get_path(filename):
            return os.path.join(rootdir, filename)

        def dump_file(filename, content, mode="w", handler=json.dump):
            absolute_fn = get_path(filename)
            with open(absolute_fn, mode) as outfile:
                handler(content, outfile)

        dump_file("meta.json", self._get_encodable_meta())
        dump_file("files.json", list(self.files.keys()))

        os.mkdir(get_path("files"))

        for k, v in self.files.items():
            dump_file(f"files/{k}", v, "wb", lambda x, y: x.dump(y))

    def to_archive(self, rootdir=None, compression="gztar"):
        filename = os.path.join(resolve_working_directory(rootdir), self.name)

        with tempfile.TemporaryDirectory() as tmpdir:
            self.to_file_structure(tmpdir)
            return shutil.make_archive(filename, compression, tmpdir)
