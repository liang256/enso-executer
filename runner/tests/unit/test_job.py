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
