import logging
from typing import List, Union
from runner.domain import events, commands
from runner.service_layer import handlers
from runner.adapters import repository


logger = logging.getLogger(__name__)


Message = Union[events.Event, commands.Command]


COMMAND_HANDLERS = {
    commands.QueryScript: handlers.query_script,
    commands.QueryMissingArgsForScript: handlers.query_missing_args_for_script,
    commands.ExecuteInstructions: handlers.execute_instructions,
}


EVENT_HANDLERS = {events.InstructionsExecuted: []}


def handle(msg: Message, repo: repository.AbstractRepository, history: List[Message]):
    queue = [msg]
    results = []

    while queue:
        m = queue.pop(0)

        # track all messages
        history.append(m)

        if isinstance(m, events.Event):
            handle_event(m, repo, queue)
        elif isinstance(m, commands.Command):
            results.append(handle_command(m, repo, queue))
        else:
            raise Exception(f"{m} is not a Command or Event")

    return results


def handle_event(
    event: events.Event, repo: repository.AbstractRepository, msg_queue: List[Message]
):
    for handler in EVENT_HANDLERS[type(event)]:
        try:
            logger.debug("handling event %s with handler %s", event, handler)
            handler(event, repo, msg_queue)
        except Exception:
            logger.exception("Exception handling event %s", event)
            continue


def handle_command(
    cmd: commands.Command,
    repo: repository.AbstractRepository,
    msg_queue: List[Message],
):
    try:
        handler = COMMAND_HANDLERS[type(cmd)]
        return handler(cmd, repo, msg_queue)
    except Exception:
        logger.exception("Exception handling command %s", cmd)
        raise
