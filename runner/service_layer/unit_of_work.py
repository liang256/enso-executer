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
        data = {}

        for job in self.jobs.list():
            data[job.id] = {"instructions": job.instructions, "state": job.state}

        with open(self.jobs.path, "w") as file:
            file.write(json.dumps(data))
