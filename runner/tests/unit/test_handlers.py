from runner.service_layer import messagebus
from runner.domain import commands, events
from runner.adapters import repository


def test_execute_script():
    instruction = ("example_script", {"data": "test message bus."})
    cmd = commands.ExecuteScript(*instruction)
    history = []

    [job_id] = messagebus.handle(cmd, repository.FileSystemRepository(), history)

    assert type(history[-1]) == events.ScriptExecuted
    assert history[-1].job_id == job_id
    assert history[-1].instructions == [instruction]
