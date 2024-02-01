from typing import List, Dict, Tuple
from runner.domain import model
from runner.adapters import repository


def get(script_ref: str, repo: repository.AbstractRepository) -> model.AbstractScript:
    return repo.get(script_ref)


def execute(
    instructions: List[Tuple],
    repo: repository.AbstractRepository,
    dispatcher: model.AbstractDispathcer,
):
    for script_ref, args in instructions:
        script = get(script_ref, repo)
        model.validate_args(script, args)
        dispatcher.execute(script, args)
