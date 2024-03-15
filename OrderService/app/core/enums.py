from enum import auto, StrEnum


class OrderStatuses(StrEnum):
    ordered = auto()
    in_progres = auto()
    finished = auto()
    canceled = auto()


class CarStatuses(StrEnum):
    ordered = auto()
    repaired = auto()
    free = auto()
