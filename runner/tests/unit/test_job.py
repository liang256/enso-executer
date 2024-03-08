import pytest
from runner.domain import model


def test_job_complete():
    job = model.Job("test-job-id", instructions=[])

    job.complete()

    assert job.state == "completed"


def test_job_fail():
    job = model.Job("test-job-id", instructions=[])

    job.fail()

    assert job.state == "failed"


def test_from_dict():
    adict = {
        "id": "dummy-id",
        "instructions": [("open_file", {"path": "/path/to/file/"})],
    }

    job = model.Job.from_dict(adict)

    assert job.id == "dummy-id"
    assert job.state == model.JobStates.Init
    assert job.instructions == (("open_file", {"path": "/path/to/file/"}),)
