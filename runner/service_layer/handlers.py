from typing import List, Tuple
from runner.domain import model, commands, events
from runner.adapters import repository, dispatcher


class ScriptNotFound(Exception):
    pass


def query_script(
    cmd: commands.QueryScript, repo, event_collector
) -> model.AbstractScript:
    script = repo.get(cmd.script_ref)
    return script


def query_missing_args_for_script(
    cmd: commands.QueryMissingArgsForScript, repo, event_collector
) -> Tuple[str, ...]:
    script = query_script(commands.QueryScript(cmd.script_ref), repo, event_collector)

    if not script:
        raise ScriptNotFound(f"{cmd.script_ref} not found in {repo}")

    return model.get_missing_args(script.required_args, cmd.args)


def execute_script(
    cmd: commands.ExecuteScript,
    repo: repository.AbstractRepository,
    event_collector,
) -> str:
    instructions = [(cmd.script_ref, cmd.args)]

    script = query_script(commands.QueryScript(cmd.script_ref), repo, event_collector)

    if not script:
        raise ScriptNotFound(f"{cmd.script_ref} not found in {repo}")

    model.validate_args(script, cmd.args)
    job_id = dispatcher.LocalDispathcer().execute(instructions, repo)
    event_collector.append(events.ScriptExecuted(job_id, instructions))
    return job_id


def handle_script_executed(event: events.ScriptExecuted, repo, event_collector):
    pass
