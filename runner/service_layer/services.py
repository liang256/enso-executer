from typing import List, Dict
from runner.domain import model
from runner.adapters import repository


class InvalidDispatcherError(Exception):
    def __init__(self, dispatcher_ref: str) -> None:
        super().__init__(f"{dispatcher_ref} is invalid.")


def get(script_ref: str, repo: repository.AbstractRepository) -> model.AbstractScript:
    return repo.get(script_ref)


def execute(
    script_ref: str,
    args: Dict,
    repo: repository.AbstractRepository,
    dispatcher: model.AbstractDispathcer,
):
    script_instance = get(script_ref, repo)
    model.validate_args(script_instance, args)
    dispatcher.execute(script_instance, args)
