import uuid
from runner.service_layer import job_services
from runner.domain import model


class FakeSession:
    def __init__(self) -> None:
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
    repo = FakeJobRepository()
    repo.add(job)
    session = FakeSession()

    job_services.execute(job.id, repo, executer=FakeExecuter(), session=session)

    assert job.state == "completed"
    assert session.commited


def test_fail_to_execute_job():
    job = model.Job(uuid.uuid4(), instructions=[])
    repo = FakeJobRepository()
    repo.add(job)
    session = FakeSession()

    job_services.execute(job.id, repo, executer=FailExecuter(), session=session)

    assert job.state == "failed"
    assert session.commited
