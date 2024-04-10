import uuid
import pytest
from dataclasses import dataclass

from runner.service_layer import services, unit_of_work
from runner.domain import model


class FakeJobUow(unit_of_work.AbstractJobUnitOfWork):
    def __init__(self, job_repo, script_repo) -> None:
        self.scripts = script_repo
        self.jobs = job_repo
        self.commited = False

    def commit(self):
        self.commited = True


class FakeJobRepository(dict):
    def add(self, job):
        self[job.id] = job


class FakeScriptRepository:
    def __init__(self, script_cls):
        self.script_cls = script_cls

    def get(self, ref):
        return self.script_cls(ref)


@dataclass
class FakeScript(model.AbstractScript):
    ref: str

    def execute(self, **kwargs):
        pass


@dataclass
class ErrorScript(model.AbstractScript):
    ref: str

    def execute(self, **kwargs):
        raise Exception("script fails")


def test_can_execute_job():
    job = model.Job(str(uuid.uuid4()), instructions=[("open_file", {})])
    job_uow = FakeJobUow(FakeJobRepository(), FakeScriptRepository(FakeScript))
    job_uow.jobs.add(job)

    services.execute(job.id, job_uow)

    assert job.state == "completed"
    assert len(job.events) == 1
    assert job.events[0].jobid == job.id
    assert job.events[0].script == "open_file"
    assert job.events[0].args == {}
    assert job_uow.commited


def test_fail_to_execute_job_since_script_error():
    job = model.Job(str(uuid.uuid4()), instructions=[("open_file", {})])
    job_uow = FakeJobUow(FakeJobRepository(), FakeScriptRepository(ErrorScript))
    job_uow.jobs.add(job)

    services.execute(job.id, job_uow)

    assert job.state == "failed"
    assert len(job.events) == 1
    assert job.events[0].message == str(Exception("script fails"))
    assert job_uow.commited


def test_fail_to_execute_job_since_job_has_completed():
    jobid = str(uuid.uuid4())
    job = model.Job(
        jobid, instructions=[("open_file", {})], state=model.JobStates.Completed
    )
    job_uow = FakeJobUow(FakeJobRepository(), FakeScriptRepository(FakeScript))
    job_uow.jobs.add(job)

    expected_msg = f"Job {jobid} has already completed."
    with pytest.raises(services.JobHasCompleted, match=expected_msg):
        services.execute(job.id, job_uow)
