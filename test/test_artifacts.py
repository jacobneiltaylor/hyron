from testconstants import TEST_ARTIFACT_CONTENT, TEST_ARTIFACT_MANIFEST_CONTENT
from hyron.artifacts import Artifact
from hyron.constants import DEF_ENCODING


def _get_test_artifact():
    artifact = Artifact(DEF_ENCODING)
    newfile = artifact["test.json"]
    newfile.write_text(TEST_ARTIFACT_CONTENT)
    artifact.close_all()
    return artifact


def test_artifact_manifest():
    artifact = _get_test_artifact()
    manifest = artifact.to_manifest()
    assert(TEST_ARTIFACT_MANIFEST_CONTENT == manifest["files"]["test.json"])
    new_artifact = Artifact.from_manifest(manifest)
    file_data = new_artifact.files["test.json"].get_contents()
    assert(file_data.decode(DEF_ENCODING) == TEST_ARTIFACT_CONTENT)
