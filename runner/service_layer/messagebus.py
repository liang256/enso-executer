from typing import List
from runner.domain import events
from runner.service_layer import handlers


class EventCollector():
    def __init__(self) -> None:
        self.events = []
        self._start_ptr = 0

    def add(self, event: events.Event):
        self.events.append(event)

    def pop_new_events(self) -> List[events.Event]:
        new_events = self.events[self._start_ptr:]
        self._start_ptr = len(self.events)
        return new_events


HANDLERS = {
    events.QueryScript: [handlers.query_script],
    events.QueryMissingArgsForScript: [handlers.query_missing_args_for_script],
    events.ExecuteScript: [handlers.execute_script],
}


def handle(event: events.Event, repo, event_collector):
    queue = [event]
    results = []
    while queue:
        e = queue.pop(0)
        for handler in HANDLERS.get(type(e), []):
            results.append(handler(e, repo, event_collector))
            queue.extend(event_collector.pop_new_events())

    return results

