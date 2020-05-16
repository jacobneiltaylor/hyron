import os
import shutil
import tempfile
from testconstants import TEST_ARTIFACT_CONTENT, TEST_ARTIFACT_MANIFEST_CONTENT
from hyron.artifacts import Artifact
from hyron.constants import DEF_ENCODING


def _get_test_artifact():
    artifact = Artifact(DEF_ENCODING)
    newfile = artifact["test.json"]
    newfile.write_text(TEST_ARTIFACT_CONTENT)
    artifact.close_all()
    return artifact


def _assert_file_structure(directory):
    def get_absolute_fn(filename):
        return os.path.join(directory, filename)

    def assert_file(filename):
        assert(os.path.exists(get_absolute_fn(filename)))

    assert_file("meta.json")
    assert_file("files.json")
    assert_file("files/test.json")


def test_artifact_manifest():
    artifact = _get_test_artifact()
    manifest = artifact.to_manifest()
    assert(TEST_ARTIFACT_MANIFEST_CONTENT == manifest["files"]["test.json"])
    new_artifact = Artifact.from_manifest(manifest)
    file_data = new_artifact.files["test.json"].get_contents()
    assert(file_data.decode(DEF_ENCODING) == TEST_ARTIFACT_CONTENT)


def test_artifact_file_structure():
    artifact = _get_test_artifact()

    with tempfile.TemporaryDirectory() as tmpdir:
        artifact.to_file_structure(tmpdir)
        _assert_file_structure(tmpdir)


def test_artifact_archive():
    artifact = _get_test_artifact()

    with tempfile.TemporaryDirectory() as working_tmpdir:
        archive_file = artifact.to_archive(working_tmpdir)
        with tempfile.TemporaryDirectory() as target_tmpdir:
            shutil.unpack_archive(archive_file, target_tmpdir, "gztar")
            with os.scandir(target_tmpdir) as entries:
                for entry in entries:
                    print(entry.name)
            _assert_file_structure(target_tmpdir)
