from dataclasses import dataclass
from typing import Dict, Tuple, List


class Event:
    pass


@dataclass
class ScriptExecuted(Event):
    jobid: str
    script: str
    args: Dict


@dataclass
class ScriptFailed(Event):
    jobid: str
    script: str
    args: Dict
    message: str
