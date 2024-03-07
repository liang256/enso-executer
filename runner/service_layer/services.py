import uuid
from typing import List, Tuple, Dict
from runner.domain import model, events
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
):
    with job_uow:
        job = job_uow.jobs.get(jobid)

        if not job:
            raise JobNotFound(jobid)

        if job.state != "init":
            raise JobHasCompleted(jobid)

        scripts = [job_uow.scripts.get(s) for s in job.scripts]

        for script, arg in zip(scripts, job.arguments):
            try:
                script.execute(arg)
                job.events.append(
                    events.ScriptExecuted(jobid=jobid, script=script.ref, args=arg)
                )
            except Exception as ex:
                job.events.append(
                    events.ScriptFailed(
                        jobid=jobid, script=script.ref, args=arg, message=str(ex)
                    )
                )
                job.fail()
                break

        if job.state == model.JobStates.Init:
            job.complete()
            job.version += 1

        job_uow.commit()
