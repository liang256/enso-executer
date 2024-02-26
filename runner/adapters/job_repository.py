import abc
from runner.domain import model


class AbstractJobRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, script: model.Job) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference: str) -> model.Job:
        raise NotImplementedError
