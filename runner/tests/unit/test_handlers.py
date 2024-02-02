from runner.service_layer import messagebus
from runner.domain import events
from runner.adapters import repository


def test_execute_script():
    instruction = ("example_script", {"data": "test message bus."})
    event = events.ExecuteScript(*instruction)
    event_collector = messagebus.EventCollector()

    [job_id] = messagebus.handle(
        event, repository.FileSystemRepository(), event_collector
    )

    assert type(event_collector.events[-1]) == events.ScriptExecuted
    assert event_collector.events[-1].job_id == job_id
    assert event_collector.events[-1].instructions == [instruction]
