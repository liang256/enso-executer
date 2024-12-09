from runner.adapters import job_repository
from runner.domain import model


def test_job_in_memory_repository_can_add_job():
    repo = job_repository.InMemoryRepository()
    job = model.Job("fake_id", "fake_script", {"fake": "args"})
    repo.add(job)

    assert len(repo.list()) == 1
    assert repo.get("fake_id") == job


def test_job_in_memory_repository_can_list_jobs():
    repo = job_repository.InMemoryRepository()
    job1 = model.Job("fake_id1", "fake_script", {"fake": "args"})
    job2 = model.Job("fake_id2", "fake_script", {"fake": "args"})
    repo.add(job1)
    repo.add(job2)

    assert len(repo.list()) == 2
    assert job1 in repo.list()
    assert job2 in repo.list()
