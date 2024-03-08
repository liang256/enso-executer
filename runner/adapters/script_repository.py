import abc
import os
import inspect
import importlib.util
import importlib.machinery
from typing import Optional
from runner.domain import model


class ScriptNotFoundError(Exception):
    pass


class LoadScriptError(Exception):
    pass


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, script: model.AbstractScript) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.AbstractScript:
        raise NotImplementedError


def snake_to_camel(snake_str):
    components = snake_str.split("_")
    return "".join(x.title() for x in components)


class FileSystemRepository(AbstractRepository):
    @property
    def default_root_dir(self):
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts"))

    def __init__(self, root_dir: Optional[str] = None):
        if root_dir and os.path.isdir(root_dir):
            self.root_dir = root_dir
        else:
            self.root_dir = self.default_root_dir

    def add(self, script: model.AbstractScript) -> str:
        src_code = inspect.getsource(script.__class__)
        file_path = os.path.join(self.root_dir, f"{script.ref}.py")
        with open(file_path, "w") as file:
            file.write(src_code)

    def get(self, reference) -> model.AbstractScript:
        file_path = os.path.join(self.root_dir, f"{reference}.py")

        if not os.path.exists(file_path):
            raise ScriptNotFoundError(f"Script file {reference}.py does not exist.")

        className = snake_to_camel(reference)
        package_path = "runner.domain.scripts"

        try:
            spec = importlib.util.spec_from_file_location(
                f"{package_path}.{reference}", file_path
            )
            tmp_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(tmp_module)
            return getattr(tmp_module, className)()
        except (AttributeError, ImportError, SyntaxError) as e:
            raise LoadScriptError(f"Error loading script {reference}: {e}")


class TessaRepository(AbstractRepository):
    def __init__(self, service) -> None:
        self.service = service

    def get(self, reference):
        # av = uri.to_asset_version(reference, self.service)
        # return model.from_py_asset_version(av)
        pass
