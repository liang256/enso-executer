from typing import List, Tuple
from runner.domain import model, commands
from runner.adapters import repository, dispatcher
from runner.service_layer import messagebus


def get(script_ref: str, repo: repository.AbstractRepository) -> model.AbstractScript:
    [script] = messagebus.handle(commands.QueryScript(script_ref), repo, [])
    return script


def execute(
    instructions: List[Tuple[str, dict]],
    repo: repository.AbstractRepository,
    dispatcher: dispatcher.AbstractDispathcer,
) -> str:
    [job_id] = messagebus.handle(
        commands.ExecuteInstructions(instructions, dispatcher), repo, []
    )
    return job_id
