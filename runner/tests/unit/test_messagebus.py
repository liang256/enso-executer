from runner.domain import events
from runner.adapters import repository
from runner.service_layer import messagebus
from dataclasses import dataclass


class FakeExampleScript:
    ref = 'example_script'


@dataclass
class FakeEvent(events.Event):
    pass


@dataclass
class NewEvent(events.Event):
    pass


def test_messagebus_can_handle():
    global_event_cnt = [0]

    def fake_handler(event, repo, collector):
        global_event_cnt[0] += 1
        collector.add(NewEvent())
        assert len(collector.events) == 1
        return FakeExampleScript()

    def increament(*args):
        global_event_cnt[0] += 1

    event_collector = messagebus.EventCollector()

    messagebus.HANDLERS = {
        FakeEvent: [fake_handler, increament],
        NewEvent: [increament]
    }

    [script, *_] = messagebus.handle(
        FakeEvent(), None, event_collector
    )

    assert type(script) == FakeExampleScript
    assert len(event_collector.events) == 1
    assert global_event_cnt[0] == 3
