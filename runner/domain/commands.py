from dataclasses import dataclass
from typing import Dict


class Command:
    pass


@dataclass
class QueryScript(Command):
    script_ref: str


@dataclass
class QueryMissingArgsForScript(Command):
    script_ref: str
    args: Dict


@dataclass
class ExecuteScript(Command):
    script_ref: str
    args: Dict
