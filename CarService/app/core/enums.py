from enum import auto, StrEnum


class CarStatuse(StrEnum):
    ordered = auto()
    repaired = auto()
    free = auto()


class Brand(StrEnum):
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


class Transmission(StrEnum):
    manual = auto()
    automatic = auto()
    automated_manual = auto()
    hydrostatic = auto()


class FuelType(StrEnum):
    gasoline = auto()
    diesel = auto()
    electric = auto()
    hybrid = auto()
    natural_gas = auto()
    ethanol = auto()


class Color(StrEnum):
    white = auto()
    black = auto()
    silver = auto()
    gray = auto()
    blue = auto()
    brown = auto()
    gold = auto()
    bronze = auto()


class Category(StrEnum):
    economy = auto()
    compact = auto()
    suv = auto()
    crossover = auto()
    luxury = auto()
    sports = auto()
    convertible = auto()
    minivan = auto()
    pickup_truck = auto()
