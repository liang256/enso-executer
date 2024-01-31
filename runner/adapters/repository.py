import abc
import os
import importlib.util
import importlib.machinery
from runner.domain import model


class ScriptNotFoundError(Exception):
    pass


class LoadScriptError(Exception):
    pass


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, reference) -> model.AbstractScript:
        raise NotImplementedError


def snake_to_camel(snake_str):
    components = snake_str.split("_")
    return "".join(x.title() for x in components)


class FileSystemRepository(AbstractRepository):
    def get(self, reference):
        scripts_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../domain/scripts")
        )
        file_path = os.path.join(scripts_dir, f"{reference}.py")

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
