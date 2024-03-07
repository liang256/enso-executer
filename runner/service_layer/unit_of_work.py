import abc
import json
from runner.adapters import job_repository


class AbstractJobUnitOfWork(abc.ABC):
    jobs: job_repository.AbstractJobRepository

    def __enter__(self) -> "AbstractJobUnitOfWork":
        return self

    def __exit__(self, *args):
        return False


class FileSystemJobUnitOfWork(AbstractJobUnitOfWork):
    def __enter__(self) -> AbstractJobUnitOfWork:
        self.jobs = job_repository.FileSystemRepository()
        return self

    def commit(self):
        old_jobs = self.jobs.read()

        adding_new_job = len(old_jobs) + 1 == len(self.jobs.list())

        if not adding_new_job:
            # assert version valid
            assert len(old_jobs) == len(self.jobs.list())
            for j in self.jobs.list():
                if j.state != old_jobs[j.id].state:
                    assert j.version == old_jobs[j.id].version + 1

        data = {}

        for job in self.jobs.list():
            data[job.id] = {
                "instructions": job.instructions,
                "state": job.state,
                "version": job.version,
            }

        with open(self.jobs.path, "w") as file:
            file.write(json.dumps(data))
