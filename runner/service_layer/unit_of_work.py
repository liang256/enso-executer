import abc
import json

from runner.adapters import job_repository, script_repository, serializers


class AbstractJobUnitOfWork(abc.ABC):
    jobs: job_repository.AbstractJobRepository
    scripts: script_repository.AbstractRepository

    def __enter__(self) -> "AbstractJobUnitOfWork":
        return self

    def __exit__(self, *args):
        return False


class FileSystemJobUnitOfWork(AbstractJobUnitOfWork):
    def __enter__(self) -> AbstractJobUnitOfWork:
        self.jobs = job_repository.FileSystemRepository()
        self.scripts = script_repository.FileSystemRepository()
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

        with open(self.jobs.path, "w") as file:
            file.write(json.dumps(self.jobs.list(), cls=serializers.JobJsonEncoder))
