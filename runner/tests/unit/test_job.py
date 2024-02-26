import pytest
from runner.domain import model


def test_job_complete():
    instructions = [
        ("open_file", {"path": "file/path"}),
        ("update_file", {"asset": "asset-uri"}),
        ("save_file", {"path": "composed/file/path"}),
        ("release_file", {"path": "composed/file/path"}),
    ]

    job = model.Job("test-job-id", instructions)

    job.complete()

    assert job.state == "completed"


def test_job_fail():
    instructions = [
        ("open_file", {"path": "file/path"}),
        ("update_file", {"asset": "asset-uri"}),
        ("save_file", {"path": "composed/file/path"}),
        ("release_file", {"path": "composed/file/path"}),
    ]

    job = model.Job("test-job-id", instructions)

    job.fail()

    assert job.state == "failed"
