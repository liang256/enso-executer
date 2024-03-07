import uuid
from runner.service_layer import services, unit_of_work
from runner.domain import model


class FakeJobUow(unit_of_work.AbstractJobUnitOfWork):
    def __init__(self) -> None:
        self.jobs = FakeJobRepository()
        self.commited = False

    def commit(self):
        self.commited = True


class FakeJobRepository(dict):
    def add(self, job):
        self[job.id] = job


class FakeExecuter:
    def __call__(self, job):
        pass


class ExecuteError(Exception):
    pass


class FailExecuter:
    def __call__(self, job):
        raise ExecuteError


def test_can_execute_job():
    job = model.Job(uuid.uuid4(), instructions=[])
    job_uow = FakeJobUow()
    job_uow.jobs.add(job)

    services.execute(job.id, job_uow, executer=FakeExecuter())

    assert job.state == "completed"
    assert job_uow.commited


def test_fail_to_execute_job():
    job = model.Job(uuid.uuid4(), instructions=[])
    job_uow = FakeJobUow()
    job_uow.jobs.add(job)

    services.execute(job.id, job_uow, executer=FailExecuter())

    assert job.state == "failed"
    assert job_uow.commited
