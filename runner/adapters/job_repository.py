import abc
import json
from typing import List
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
        self._jobs = {}

        with open(self.path) as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError:
                data = {}

        for jobid in data:
            self._jobs[jobid] = model.Job(
                jobid, data[jobid]["instructions"], data[jobid]["state"]
            )

    def add(self, job: model.Job) -> None:
        self._jobs[job.id] = job

    def get(self, reference: str) -> model.Job:
        return self._jobs.get(reference, None)

    def list(self) -> List[model.Job]:
        return list(self._jobs.values())

    @property
    def path(self):
        # Assuming __file__ is the path to the current script
        # Get the parent directory of the script
        script_directory = Path(__file__).parent

        # Construct the path to jobs.json relative to the script's directory
        jobs_file_path = script_directory / "jobs.json"

        return jobs_file_path
