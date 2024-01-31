import abc
from typing import Dict, Tuple
from dataclasses import dataclass


dataclass(frozen=True)


class Instruction:
    script_ref: str
    args: Dict[str, str]
    dispatcher: str


class MissingRequiredArguments(Exception):
    def __init__(self, class_name: str, missing_args: Tuple[str, ...]):
        super().__init__(
            f"Missing required arguments in {class_name}: {', '.join(missing_args)}"
        )


class AbstractScript(abc.ABC):
    @abc.abstractmethod
    def execute(self, args: Dict[str, str]) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_required_args(self) -> Tuple[str, ...]:
        raise NotImplementedError


def validate_args(script: AbstractScript, args: Dict[str, str]):
    missing_args = get_missing_args(script.get_required_args(), args)
    if missing_args:
        raise MissingRequiredArguments(script.__class__.__name__, missing_args)


def get_missing_args(
    required: Tuple[str, ...], args: Dict[str, str]
) -> Tuple[str, ...]:
    return tuple(req for req in required if req not in args)


def hash_str_and_dict(s: str, d: Dict):
    dict_hash = hash(tuple(sorted(d.items())))
    return hash((s, dict_hash))


class AbstractDispathcer(abc.ABC):
    @abc.abstractmethod
    def execute(self, script: AbstractScript, args: Dict[str, str]):
        raise NotImplementedError

    @abc.abstractmethod
    def has_executed(self, script: AbstractScript, args) -> bool:
        raise NotImplementedError


class LocalDispathcer(AbstractDispathcer):
    def __init__(self) -> None:
        super().__init__()
        self._executed = set()

    def execute(self, script: AbstractScript, args: Dict[str, str]):
        script.execute(args)
        self._executed.add(hash_str_and_dict(script, args))

    def has_executed(self, script: AbstractScript, args) -> bool:
        return hash_str_and_dict(script, args) in self._executed
