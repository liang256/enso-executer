import pytest
import os

from runner.domain import model
from runner.service_layer import unit_of_work


def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


@pytest.fixture
def job_json_file_path(tmp_path):
    return os.path.join(tmp_path, "test_jobs.json")


def test_can_commit(job_json_file_path):
    uof = unit_of_work.FileSystemJobUnitOfWork(job_json_file_path)
    with uof:
        uof.jobs.add(model.Job(id="dummy-job-id", instructions=[]))
        uof.commit()

    with uof:
        job = uof.jobs.get("dummy-job-id")
        assert isinstance(job, model.Job)
        assert job.id == "dummy-job-id"
        assert job.instructions == tuple()
        assert job.state == model.JobStates.Init

    remove_file(job_json_file_path)
