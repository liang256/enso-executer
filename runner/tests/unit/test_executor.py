from runner.adapters import executer
from runner.domain import model


class FakeScript:
    def __init__(self, script_name: str) -> None:
        self.ref = script_name

    def execute(self, args):
        pass


class FakeScriptRepo(dict):
    def add(self, script_name: str):
        self[script_name] = FakeScript(script_name)


def test_simple_executor():
    instructions = [
        ("open_file", {"path": "file/to/open"}),
        ("update_file", {}),
        ("release", {}),
    ]
    job = model.Job("job-id", instructions)

    repo = FakeScriptRepo()
    for script_name, _ in instructions:
        repo.add(script_name)

    execute = executer.SimpleExecuter(repo)
    execute(job)

    assert len(job.events) == 3
