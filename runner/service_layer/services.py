from typing import List, Dict, Tuple
from runner.domain import model
from runner.adapters import repository, dispatcher


def get(script_ref: str, repo: repository.AbstractRepository) -> model.AbstractScript:
    return repo.get(script_ref)


def execute(
    instructions: List[Tuple],
    repo: repository.AbstractRepository,
    dispatcher: dispatcher.AbstractDispathcer,
) -> str:
    job = model.Job.from_primitive(instructions)
    job_id = dispatcher.execute(job, repo)
    return job_id
