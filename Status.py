from enum import Enum, auto

class Status(Enum):
    created = auto()
    inProcess = auto()
    cancelled = auto()
    done = auto()
    timeIsOver = auto()
