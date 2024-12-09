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


def get(jobid: str, job_uow: unit_of_work.AbstractJobUnitOfWork) -> Dict:
    with job_uow:
        try:
            job = job_uow.jobs.get(jobid)
        except job_repository.JobNotFound:
            return None
        return job.to_dict()


def execute(
    jobid: str,
    job_uow: unit_of_work.AbstractJobUnitOfWork,
):
    """
    Executes a job with the given job ID within the provided unit of work.

    Args:
        jobid (str): The ID of the job to execute.
        job_uow (unit_of_work.AbstractJobUnitOfWork): The unit of work context for job execution.
    Raises:
        JobHasCompleted: If the job has already completed.
        job_repository.JobNotFound: If the job is not found in the unit of work.

    The function retrieves the job using the job ID and executes each instruction in the job.
    If an instruction fails, it logs the failure event and marks the job as failed.
    If all instructions are executed successfully, it marks the job as complete and increments the job version.
    Finally, it commits the changes in the unit of work.
    """
    with job_uow:
        job = job_uow.jobs.get(jobid)

        if job.state != model.JobStates.Init:
            raise JobHasCompleted(f"Job {jobid} has already completed.")

        for inctruction in job.instructions:
            script_ref, arg = inctruction.script, inctruction.arguments
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
