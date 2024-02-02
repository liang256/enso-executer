from runner.service_layer.messagebus import EventCollector
from runner.domain import events


def test_event_collector_can_pop_new_events():
    collector = EventCollector()

    for _ in range(10):
        collector.add(events.Event())

    assert len(collector.events) == 10

    new_events = collector.pop_new_events()

    assert len(new_events) == 10
