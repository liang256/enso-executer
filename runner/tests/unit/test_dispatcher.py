from runner.domain import model
from typing import Dict, Tuple


class FakeScript(model.AbstractScript):
    ref = "fake_script"

    def execute(self, args: Dict[str, str]) -> None:
        pass

    def get_required_args(self) -> Tuple[str, ...]:
        return tuple()


def test_hash_str_and_dict_consistency():
    s = "example"
    d = {"a": 1, "b": 2, "c": 3}
    assert model.hash_str_and_dict(s, d) == model.hash_str_and_dict(s, d)


def test_hash_str_and_dict_uniqueness():
    s1, s2 = "example1", "example2"
    d1, d2 = {"a": 1, "b": 2}, {"a": 3, "b": 4}
    assert model.hash_str_and_dict(s1, d1) != model.hash_str_and_dict(s2, d2)


def test_hash_str_and_dict_order_independence():
    s = "example"
    d1 = {"a": 1, "b": 2, "c": 3}
    d2 = {"b": 2, "c": 3, "a": 1}  # Same as d1 but different order
    assert model.hash_str_and_dict(s, d1) == model.hash_str_and_dict(s, d2)


def test_local_dispatcher_execute():
    dispatcher = model.LocalDispathcer()
    script = FakeScript()
    dispatcher.execute(script, {})

    assert dispatcher.has_executed(script, {})
