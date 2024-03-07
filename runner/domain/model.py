import abc
from typing import Dict, Tuple, List
from dataclasses import dataclass


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


class MissingRequiredArguments(Exception):
    def __init__(self, class_name: str, missing_args: Tuple[str, ...]):
        super().__init__(
            f"Missing required arguments in {class_name}: {', '.join(missing_args)}"
        )


class AbstractScript(abc.ABC):
    ref: str  # script reference
    required_args: Tuple[str, ...]  # required arguments

    @abc.abstractmethod
    def execute(self, args: Dict) -> None:
        raise NotImplementedError

    def can_execute(self, args: Dict) -> bool:
        return len(get_missing_args(self.required_args, args)) == 0


def validate_args(script: AbstractScript, args: Dict):
    missing_args = get_missing_args(script.required_args, args)
    if missing_args:
        raise MissingRequiredArguments(script.__class__.__name__, missing_args)


def get_missing_args(required: Tuple[str, ...], args: Dict) -> Tuple[str, ...]:
    return tuple(req for req in required if req not in args)
