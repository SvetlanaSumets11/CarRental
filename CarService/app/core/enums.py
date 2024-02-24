from enum import auto, StrEnum


class Statuses(StrEnum):
    ordered = auto()
    repaired = auto()
    free = auto()


class Brands(StrEnum):
    toyota = auto()
    honda = auto()
    ford = auto()
    bmw = auto()
    mercedes_benz = auto()
    volkswagen = auto()
    nissan = auto()
    hyundai = auto()
    audi = auto()
    subaru = auto()
    kia = auto()
    tesla = auto()
    mazda = auto()


class Transmissions(StrEnum):
    manual = auto()
    automatic = auto()
    automated_manual = auto()
    hydrostatic = auto()


class FuelTypes(StrEnum):
    gasoline = auto()
    diesel = auto()
    electric = auto()
    hybrid = auto()
    natural_gas = auto()
    ethanol = auto()


class Colors(StrEnum):
    white = auto()
    black = auto()
    silver = auto()
    gray = auto()
    blue = auto()
    brown = auto()
    gold = auto()
    bronze = auto()


class Categories(StrEnum):
    economy = auto()
    compact = auto()
    suv = auto()
    crossover = auto()
    luxury = auto()
    sports = auto()
    convertible = auto()
    minivan = auto()
    pickup_truck = auto()
