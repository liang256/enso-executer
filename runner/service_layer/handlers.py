from typing import List, Tuple
from runner.domain import model, commands, events
from runner.adapters import repository, dispatcher


class ScriptNotFound(Exception):
    pass


def query_script(cmd: commands.QueryScript, repo, msg_queue) -> model.AbstractScript:
    return repo.get(cmd.script_ref)


def query_missing_args_for_script(
    cmd: commands.QueryMissingArgsForScript, repo, msg_queue
) -> Tuple[str, ...]:
    script = query_script(commands.QueryScript(cmd.script_ref), repo, msg_queue)
    return model.get_missing_args(script.required_args, cmd.args)


def execute_instructions(cmd: commands.ExecuteInstructions, repo, msg_queue):
    job_id = cmd.dispatcher.execute(cmd.instructions, repo)
    msg_queue.append(events.InstructionsExecuted(job_id, cmd.instructions))
    return job_id


def handle_instructions_executed(event: events.InstructionsExecuted, repo, msg_queue):
    pass
