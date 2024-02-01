from typing import List, Tuple
from runner.domain import model
from runner.adapters import repository, dispatcher


def get(script_ref: str, repo: repository.AbstractRepository) -> model.AbstractScript:
    return repo.get(script_ref)


def execute(
    instructions: List[Tuple[str, dict]],
    repo: repository.AbstractRepository,
    dispatcher: dispatcher.AbstractDispathcer,
) -> str:
    job_id = dispatcher.execute(instructions, repo)
    return job_id
