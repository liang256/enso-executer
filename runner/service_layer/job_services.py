import uuid
from typing import List, Tuple, Dict
from runner.adapters import executer
from runner.domain import model
from runner.service_layer import unit_of_work


class JobHasCompleted(Exception):
    pass


class JobNotFound(Exception):
    pass


class JobAlreadyExists(Exception):
    pass


def add(
    instructions: List[Tuple[str, Dict]],
    job_uow: unit_of_work.AbstractJobUnitOfWork,
):
    jobid = str(uuid.uuid4())
    with job_uow:
        while job_uow.jobs.get(jobid):
            jobid = str(uuid.uuid4())
        job = model.Job(jobid, instructions, "init")
        job_uow.jobs.add(job)
        job_uow.commit()
    return jobid


def execute(
    jobid: str,
    job_uow: unit_of_work.AbstractJobUnitOfWork,
    executer: executer.AbstractExecuter,
):
    with job_uow:
        job = job_uow.jobs.get(jobid)

        if not job:
            raise JobNotFound(jobid)

        if job.state != "init":
            raise JobHasCompleted(jobid)

        try:
            executer(job)
            job.complete()
        except Exception:
            job.fail()
        finally:
            job_uow.commit()
