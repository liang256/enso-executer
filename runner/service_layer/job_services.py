import uuid
from typing import List, Tuple, Dict
from runner.adapters import job_repository
from runner.domain import model
from runner.service_layer import unit_of_work


class JobHasCompleted(Exception):
    pass


def add(
    jobid: str,
    instructions: List[Tuple[str, Dict]],
    job_uow: unit_of_work.AbstractJobUnitOfWork,
):
    with job_uow:
        job = job_uow.jobs.get(jobid)

        if not job:
            job = model.Job(jobid, instructions, "init")
            job_uow.jobs.add(job)

        job_uow.commit()

    return jobid


def execute(jobid: str, job_uow: unit_of_work.AbstractJobUnitOfWork, executer):
    with job_uow:
        job = job_uow.jobs.get(jobid)

        if job.state == "completed":
            raise JobHasCompleted(jobid)

        try:
            executer(job)
            job.complete()
        except Exception as ex:
            job.fail()
        finally:
            job_uow.commit()
