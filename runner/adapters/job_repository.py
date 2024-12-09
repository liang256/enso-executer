import abc
import json
import os
from typing import List, Dict
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
    def __init__(self, json_file_path: str = "") -> None:
        self._path = json_file_path
        self._jobs = self.read()

    def read(self) -> Dict[str, model.Job]:
        data = []
        if os.path.exists(self.path):
            with open(self.path) as file:
                try:
                    data = json.load(file)
                except json.decoder.JSONDecodeError:
                    data = []

        job_list = [model.Job.from_dict(row) for row in data]
        return {j.id: j for j in job_list}

    def add(self, job: model.Job) -> None:
        self._jobs[job.id] = job

    def get(self, reference: str) -> model.Job:
        job = self._jobs.get(reference, None)
        if job is None:
            raise JobNotFound(f"Can not find job {reference}")
        return job

    def list(self) -> List[model.Job]:
        return list(self._jobs.values())

    @property
    def path(self):
        if self._path:
            return self._path
        self._path = self.default_path
        return self._path

    @property
    def default_path(self):
        # Assuming __file__ is the path to the current script
        # Get the parent directory of the script
        script_directory = Path(__file__).parent

        # Construct the path to jobs.json relative to the script's directory
        jobs_file_path = script_directory / "jobs.json"

        return jobs_file_path


class InMemoryRepository(AbstractJobRepository):
    def __init__(self):
        self._jobs = {}

    def add(self, job: model.Job) -> None:
        self._jobs[job.id] = job

    def get(self, reference: str) -> model.Job:
        job = self._jobs.get(reference, None)
        if job is None:
            raise JobNotFound(f"Can not find job {reference}")
        return job

    def list(self) -> List[model.Job]:
        return list(self._jobs.values())

    def __len__(self) -> int:
        return len(self._jobs)

    def __iter__(self):
        return iter(self._jobs.values())
