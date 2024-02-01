from typing import Dict
from runner.service_layer import services
from runner.domain import model


class FakeRepository(dict):
    def list(self):
        return self.values()


class FakeDispatcher(set):
    def execute(self, script_instance: model.AbstractScript, args: Dict):
        self.add(model.hash_str_and_dict(script_instance.ref, args))

    def has_executed(self, script_instance: model.AbstractScript, args: Dict) -> bool:
        return model.hash_str_and_dict(script_instance.ref, args) in self


class FakeScript(model.AbstractScript):
    required_args = tuple()

    def __init__(self, ref: str) -> None:
        self.ref = ref

    def execute(self, args: Dict) -> None:
        print(f"execute {self.ref}")


def test_get():
    script_ref = "fake_script"
    repo = FakeRepository(fake_script=FakeScript(script_ref))

    script_instance = services.get(script_ref, repo)

    assert script_instance is not None
    assert script_instance.ref == script_ref


def test_execute():
    repo = FakeRepository(
        open_file=FakeScript("open_file"),
        update_file=FakeScript("update_file"),
        release_assets=FakeScript("release_assets"),
    )
    dispatcher = FakeDispatcher()
    instructions = [("open_file", {}), ("update_file", {}), ("release_assets", {})]

    services.execute(instructions, repo, dispatcher)

    for script in repo.list():
        assert dispatcher.has_executed(script, {})
