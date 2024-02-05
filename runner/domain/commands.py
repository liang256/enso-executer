from dataclasses import dataclass
from typing import Dict
from runner.adapters import dispatcher


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
class ExecuteInstructions(Command):
    instructions: tuple
    dispatcher: dispatcher.AbstractDispathcer
