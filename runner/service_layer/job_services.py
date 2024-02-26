import uuid
from typing import List, Tuple, Dict
from runner.adapters import job_repository
from runner.domain import model


def add(
    instructions: List[Tuple[str, Dict]],
    job_repo: job_repository.AbstractJobRepository,
    session,
):
    jobid = uuid.uuid4()
    job = model.Job(jobid, instructions)
    job_repo.add(job)
    session.commit()
    return jobid


def execute(
    jobid: str, job_repo: job_repository.AbstractJobRepository, executer, session
):
    job = job_repo.get(jobid)
    try:
        executer(job)
        job.complete()
    except Exception as ex:
        job.fail()
    finally:
        session.commit()
