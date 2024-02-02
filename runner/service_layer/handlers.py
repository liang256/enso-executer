from typing import List, Tuple
from runner.domain import model, events
from runner.adapters import repository, dispatcher


def query_script(
    event: events.QueryScript, repo, event_collector
) -> model.AbstractScript:
    script = repo.get(event.script_ref)
    if not script:
        event_collector.add(events.ScriptNotFound(event.script_ref))
    return script


def query_missing_args_for_script(
    event: events.QueryMissingArgsForScript, repo, event_collector
) -> Tuple[str, ...]:
    script = query_script(events.QueryScript(event.script_ref), repo, event_collector)
    if not script:
        return

    return model.get_missing_args(script.required_args, event.args)


def execute_script(
    event: events.ExecuteScript,
    repo: repository.AbstractRepository,
    event_collector,
) -> str:
    instructions = [(event.script_ref, event.args)]

    missing_args = query_missing_args_for_script(
        events.QueryMissingArgsForScript(event.script_ref, event.args),
        repo,
        event_collector,
    )

    if missing_args:
        event_collector.add(
            events.MissingRequiredArgs(event.script_ref, missing_args)
        )
        return

    job_id = dispatcher.LocalDispathcer().execute(instructions, repo)
    event_collector.add(events.ScriptExecuted(job_id, instructions))
    return job_id
