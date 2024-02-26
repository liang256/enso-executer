import abc
from typing import Dict, Tuple, List
from dataclasses import dataclass


@dataclass(frozen=True)
class Instruction:
    script_ref: str
    args: Dict


class Job:
    def __init__(
        self, jobid: str, instructions: List[Tuple[str, Dict]], state: str = "init"
    ) -> None:
        self._instructions = tuple(instructions)
        self.state = "init"
        self.events = []
        self.id = jobid

    def complete(self):
        self.state = "completed"

    def fail(self):
        self.state = "failed"


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
