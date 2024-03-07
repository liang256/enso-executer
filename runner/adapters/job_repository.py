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
    def __init__(self) -> None:
        self._jobs = self.read()

    def read(self) -> Dict[str, model.Job]:
        with open(self.path) as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError:
                data = {}

        return model.Job.create_from_dict(data)

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

        if not os.path.exists(jobs_file_path):
            with open(jobs_file_path, "w") as file:
                file.write(json.dumps({}))

        return jobs_file_path
