import abc
from typing import Dict, Tuple, List


class JobStates:
    Init = "init"
    Failed = "failed"
    Completed = "completed"


class Job:
    def __init__(
        self,
        id: str,
        instructions: List[Tuple[str, Dict]],
        state: str = JobStates.Init,
        version: int = 1,
    ) -> None:
        self.instructions = tuple(instructions)
        self.state = state if state else JobStates.Init
        self.events = []
        self.id = id
        self.version = version

    @property
    def scripts(self) -> List[str]:
        return [s for s, _ in self.instructions]

    @property
    def arguments(self) -> List[Dict]:
        return [arg for _, arg in self.instructions]

    def complete(self):
        self.state = JobStates.Completed

    def fail(self):
        self.state = JobStates.Failed

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    @classmethod
    def from_dict(cls, adict):
        return cls(**adict)


class AbstractScript(abc.ABC):
    ref: str  # script reference

    @abc.abstractmethod
    def execute(self, **kwargs) -> None:
        raise NotImplementedError
