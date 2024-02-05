from runner.service_layer import messagebus
from runner.domain import commands, events
from runner.adapters import repository, dispatcher


def test_execute_instructions():
    instructions = [("example_script", {"data": "test message bus."})]
    cmd = commands.ExecuteInstructions(instructions, dispatcher.LocalDispathcer())
    history = []

    [job_id] = messagebus.handle(cmd, repository.FileSystemRepository(), history)

    assert type(history[-1]) == events.InstructionsExecuted
    assert history[-1].job_id == job_id
    assert history[-1].instructions == instructions
