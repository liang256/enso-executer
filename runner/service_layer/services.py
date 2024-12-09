import uuid
from typing import List, Tuple, Dict
from runner.domain import model, events
from runner.service_layer import unit_of_work
from runner.adapters import job_repository


class JobHasCompleted(Exception):
    pass


def add(
    raw_instructions: List[Tuple[str, Dict]],
    job_uow: unit_of_work.AbstractJobUnitOfWork,
):
    jobid = str(uuid.uuid4())
    instructions = [model.Instruction(script, arg) for script, arg in raw_instructions]
    with job_uow:
        while True:
            try:
                job = job_uow.jobs.get(jobid)
            except job_repository.JobNotFound:
                break
            jobid = str(uuid.uuid4())
        job = model.Job(jobid, instructions, model.JobStates.Init)
        job_uow.jobs.add(job)
        job_uow.commit()
    return jobid


def execute(
    jobid: str,
    job_uow: unit_of_work.AbstractJobUnitOfWork,
):
    with job_uow:
        job = job_uow.jobs.get(jobid)

        if job.state != model.JobStates.Init:
            raise JobHasCompleted(f"Job {jobid} has already completed.")

        for script_ref, arg in job.instructions:
            script = job_uow.scripts.get(script_ref)

            try:
                script.execute(**arg)
                job.events.append(
                    events.ScriptExecuted(jobid=jobid, script=script.ref, args=arg)
                )
            except Exception as ex:
                job.events.append(
                    events.ScriptFailed(
                        jobid=jobid, script=script_ref, args=arg, message=str(ex)
                    )
                )
                job.fail()
                break

        if job.state == model.JobStates.Init:
            job.complete()
            job.version += 1

        job_uow.commit()
