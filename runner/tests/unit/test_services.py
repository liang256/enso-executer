from typing import Dict, Tuple
from runner.service_layer import services
from runner.adapters import repository
from runner.domain import model


class FakeRepository(dict):
    pass


class FakeDispatcher(set):
    def execute(self, script_instance: model.AbstractScript, args: Dict):
        self.add(model.hash_str_and_dict(script_instance.ref, args))

    def has_executed(self, script_instance: model.AbstractScript, args: Dict) -> bool:
        return model.hash_str_and_dict(script_instance.ref, args) in self


class FakeScript(model.AbstractScript):
    ref = "fake_script"

    def execute(self, args: Dict[str, str]) -> None:
        pass

    def get_required_args(self) -> Tuple[str, ...]:
        return tuple()


def test_get():
    script_ref = "fake_script"
    repo = FakeRepository(fake_script=FakeScript())

    script_instance = services.get(script_ref, repo)

    assert script_instance is not None
    assert script_instance.ref == script_ref


def test_execute():
    script_ref = "fake_script"
    args = {"data": "fake_data"}
    repo = FakeRepository(fake_script=FakeScript())
    dispatcher = FakeDispatcher()

    script_instance = services.get(script_ref, repo)

    services.execute(script_ref, args, repo, dispatcher)

    assert dispatcher.has_executed(script_instance, args)
