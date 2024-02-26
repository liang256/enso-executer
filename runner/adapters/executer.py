import abc
from runner.domain import model, events
from runner.adapters import repository as script_repository


class AbstractExecuter(abc.ABC):
    scripts: script_repository.AbstractRepository

    @abc.abstractmethod
    def __call__(self, job: model.Job) -> bool:
        raise NotImplementedError


class SimpleExecuter(AbstractExecuter):
    def __init__(self, script_repo: script_repository.AbstractRepository) -> None:
        self.scripts = script_repo

    def __call__(self, job: model.Job) -> bool:
        for script_name, args in job.instructions:
            script = self.scripts.get(script_name)
            script.execute(args)
            job.events.append(events.ScriptExecuted(job.id, script_name, args))
