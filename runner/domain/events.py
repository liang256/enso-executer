from dataclasses import dataclass
from typing import Dict, Tuple, List


class Event:
    pass


@dataclass
class InstructionsExecuted(Event):
    job_id: str
    instructions: List[Tuple[str, Dict]]
