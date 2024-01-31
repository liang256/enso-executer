import pytest
import os
from runner.adapters import repository


def create_class_file(package_path, base_name, class_content):
    file_name = f"{base_name}.py"
    file_path = os.path.join(package_path, file_name)
    with open(file_path, "w") as file:
        file.write(class_content)
    return file_path


def remove_class_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


@pytest.fixture
def fake_script_file():
    package_path = os.path.join(os.path.dirname(__file__), "../../domain/scripts")
    base_name = "fake_script"
    class_content = "class FakeScript:\n    pass\n"

    file_path = create_class_file(package_path, base_name, class_content)

    # Yield the file path to the test
    yield file_path

    # Clean up: remove the class file
    remove_class_file(file_path)


@pytest.fixture
def unloadable_script_file():
    package_path = os.path.join(os.path.dirname(__file__), "../../domain/scripts")
    base_name = "unloadable_script"
    class_content = "This script can't be loaded."

    file_path = create_class_file(package_path, base_name, class_content)

    # Yield the file path to the test
    yield file_path

    # Clean up: remove the class file
    remove_class_file(file_path)


def test_file_system_repository_can_get_script(fake_script_file):
    ref = "fake_script"
    repo = repository.FileSystemRepository()
    retrieved_script = repo.get(ref)

    assert retrieved_script is not None
    assert retrieved_script.__class__.__name__ == "FakeScript"


def test_file_system_repository_fail_to_get_script_since_file_not_exist():
    ref = "non_exist_script"
    expected_msg = f"Script file {ref}.py does not exist."
    with pytest.raises(repository.ScriptNotFoundError, match=expected_msg):
        repository.FileSystemRepository().get(ref)


def test_file_system_repository_fail_to_load_script(unloadable_script_file):
    ref = "unloadable_script"
    expected_msg = f"Error loading script {ref}"
    with pytest.raises(repository.LoadScriptError, match=expected_msg):
        repository.FileSystemRepository().get(ref)
