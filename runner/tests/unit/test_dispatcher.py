from runner.domain import model
from runner.adapters import dispatcher
from typing import Dict


class FakeScript(model.AbstractScript):
    ref = "fake_script"
    required_args = tuple()

    def execute(self, args: Dict) -> None:
        pass


class FakeRepository:
    def get(self, ref):
        return FakeScript()


def test_local_dispatcher_execute():
    d = dispatcher.LocalDispathcer()
    instructions = [
        ("open_file", {}),
        ("update_file", {}),
        ("save_file", {}),
    ]
    job_id = d.execute(instructions, FakeRepository())

    assert d.has_executed(job_id)
