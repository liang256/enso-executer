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
    
    def commit(self):
        raise NotImplementedError

class FileSystemJobUnitOfWork(AbstractJobUnitOfWork):
    def __init__(self, storage_json_path: str = ""):
        self._file_path = storage_json_path

    def __enter__(self) -> AbstractJobUnitOfWork:
        self.jobs = job_repository.FileSystemRepository(self._file_path)
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

class InMemoryJobUnitOfWork(AbstractJobUnitOfWork):
    def __init__(self):
        self.jobs = job_repository.InMemoryRepository()
        self.scripts = script_repository.FileSystemRepository()

    def commit(self):
        pass    