import pytest
import os
from typing import Dict
from runner.adapters import script_repository
from runner.domain import model


class FileTestingUnionOfWork:
    def __init__(self, root_dir: str, base_name: str, content: str):
        self.root_dir = root_dir
        self.base_name = base_name
        self.content = content

    @property
    def file_path(self):
        return os.path.join(self.root_dir, f"{self.base_name}.py")

    def __enter__(self):
        with open(self.file_path, "w") as f:
            f.write(self.content)

    def __exit__(self, *args):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)


def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


@pytest.fixture
def package_path(tmp_path):
    root_path = os.path.join(tmp_path, "scripts")
    if not os.path.isdir(root_path):
        os.makedirs(root_path, exist_ok=True)
    assert os.path.isdir(root_path)
    return root_path


class FakeNewScript(model.AbstractScript):
    ref = "fake_new_script"
    required_args = tuple()

    def execute(self, args: Dict) -> None:
        # check if this line be written into file
        pass


def test_file_system_repository_can_add_script(package_path):
    new_script = FakeNewScript()
    repo = script_repository.FileSystemRepository(package_path)
    repo.add(new_script)

    expected_script_path = os.path.join(package_path, f"{new_script.ref}.py")

    assert os.path.exists(expected_script_path)
    with open(expected_script_path) as f:
        assert "# check if this line be written into file" in f.read()
    remove_file(expected_script_path)


def test_file_system_repository_can_get_script(package_path):
    ref = "fake_script"
    content = "class FakeScript:\n    pass\n"
    uow = FileTestingUnionOfWork(package_path, ref, content)
    repo = script_repository.FileSystemRepository(package_path)

    with uow:
        retrieved_script = repo.get(ref)

        assert retrieved_script is not None
        assert retrieved_script.__class__.__name__ == "FakeScript"


def test_file_system_repository_fail_to_get_script_since_file_not_exist(package_path):
    ref = "non_exist_script"
    expected_msg = f"Script file {ref}.py does not exist."
    with pytest.raises(script_repository.ScriptNotFoundError, match=expected_msg):
        script_repository.FileSystemRepository(package_path).get(ref)


def test_file_system_repository_fail_to_load_script(package_path):
    ref = "unloadable_script"
    content = "invalid python script file"
    expected_msg = f"Error loading script {ref}"

    with FileTestingUnionOfWork(package_path, ref, content):
        with pytest.raises(script_repository.LoadScriptError, match=expected_msg):
            script_repository.FileSystemRepository(package_path).get(ref)
