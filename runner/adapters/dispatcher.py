import abc
import uuid
from runner.domain import model
from runner.adapters import repository


def generate_job_id():
    return uuid.uuid4()


class AbstractDispathcer(abc.ABC):
    @abc.abstractmethod
    def execute(self, job: model.Job, repo: repository.AbstractRepository) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def has_executed(self, job_id: str) -> bool:
        raise NotImplementedError


class LocalDispathcer(AbstractDispathcer):
    def __init__(self) -> None:
        super().__init__()
        self._executed = set()

    def execute(self, job: model.Job, repo: repository.AbstractRepository) -> str:
        for instruction in job:
            script = repo.get(instruction.script_ref)
            model.validate_args(script, instruction.args)
            script.execute(instruction.args)

        job_id = generate_job_id()
        self._executed.add(job_id)
        return job_id

    def has_executed(self, job_id: str) -> bool:
        return job_id in self._executed
