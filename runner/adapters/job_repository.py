import abc
import json
from pathlib import Path
from runner.domain import model


class JobNotFound(Exception):
    pass


class AbstractJobRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, job: model.Job) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference: str) -> model.Job:
        raise NotImplementedError


class FileSystemRepository(AbstractJobRepository):
    def __init__(self) -> None:
        with open(self.path) as file:
            data = json.load(file)
            self.jobs = {}
            for jobid in data:
                self.jobs[jobid] = model.Job(
                    jobid, data[jobid]["instructions"], data[jobid]["state"]
                )

    def add(self, job: model.Job) -> None:
        self.jobs[job.id] = job

    def get(self, reference: str) -> model.Job:
        if reference not in self.jobs:
            raise JobNotFound(reference)

        return self.jobs.get(reference)

    @property
    def path(self):
        # Assuming __file__ is the path to the current script
        # Get the parent directory of the script
        script_directory = Path(__file__).parent

        # Construct the path to jobs.json relative to the script's directory
        jobs_file_path = script_directory / "jobs.json"

        return jobs_file_path
