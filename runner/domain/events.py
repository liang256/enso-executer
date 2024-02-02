from dataclasses import dataclass
from typing import Dict, Tuple, List


class Event:
    pass


@dataclass
class QueryScript(Event):
    script_ref: str


@dataclass
class ScriptNotFound(Event):
    script_ref: str


@dataclass
class QueryMissingArgsForScript(Event):
    script_ref: str
    args: Dict


@dataclass
class ExecuteScript(Event):
    script_ref: str
    args: Dict


@dataclass
class ScriptExecuted(Event):
    job_id: str
    instructions: List[Tuple[str, Dict]]


@dataclass
class MissingRequiredArgs(Event):
    script_ref: str
    missing_args: tuple
