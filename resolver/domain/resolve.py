from typing import List
from dataclasses import dataclass


dataclass(unsafe_hash=True)


class ACPTree:
    uri: str
    children: List["ACPTree"]


def instructions_from_acp_tree(acp_tree: ACPTree) -> List[str]:
    pass


def instructions_by_acp_workflow(acp_uri: str) -> List[str]:
    pass


def instructions_by_shot_workflow(tmp_file: str, shot_uri: str) -> List[str]:
    pass
