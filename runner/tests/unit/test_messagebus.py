from runner.domain import events, commands
from runner.adapters import repository
from runner.service_layer import messagebus
from dataclasses import dataclass


@dataclass
class IncreamentCommand(commands.Command):
    pass


@dataclass
class Increamented(events.Event):
    pass


def test_messagebus_can_handle():
    global_handle_cnt = [0] # track total times in handlers

    def broadcast_event(event, repo, msg_queue):
        global_handle_cnt[0] += 1

    def do_other_thing_after_increament(event, repo, msg_queue):
        global_handle_cnt[0] += 1

    def increament(cmd, repo, msg_queue):
        global_handle_cnt[0] += 1
        msg_queue.append(Increamented())

    history = []

    messagebus.COMMAND_HANDLERS = {IncreamentCommand: increament}

    messagebus.EVENT_HANDLERS = {
        Increamented: [broadcast_event, do_other_thing_after_increament]
    }

    results = messagebus.handle(IncreamentCommand(), None, history)

    assert len(history) == 2
    assert type(history[0]) == IncreamentCommand
    assert type(history[1]) == Increamented
    assert global_handle_cnt[0] == 3
