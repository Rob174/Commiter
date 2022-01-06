from dataclasses import dataclass
from enums import Enum


class StatusEnum(Enum):
    TODO = "TODO"
    DONE = 'DONE'
    BUILDING = "BUILDING"
    RUNNING = "RUNNING"
    IN_PROGRESS = "IN_PROGRESS"
    WAITING = "WAITING"
    PROBLEM = "PROBLEM"
    TO_IMPROVE = "TO_IMPROVE"
    PAUSE = "PAUSE"
    RELEASE = "RELEASE"

