from enum import StrEnum


class Statuses(StrEnum):
    ordered = 'ordered'
    repaired = 'repaired'
    free = 'free'


class Brands(StrEnum):
    toyota = 'Toyota'
    honda = 'Honda'
    ford = 'Ford'
    bmw = 'BMW'
    mercedes_benz = 'Mercedes-Benz'
    volkswagen = 'Volkswagen'
    nissan = 'Nissan'
    hyundai = 'Hyundai'
    audi = 'Audi'
    subaru = 'Subaru'
    kia = 'Kia'
    tesla = 'Tesla'
    mazda = 'Mazda'


class Transmissions(StrEnum):
    manual = 'Manual'
    automatic = 'Automatic'
    automated_manual = 'Automated Manual'
    hydrostatic = 'Hydrostatic'


class FuelTypes(StrEnum):
    gasoline = 'Gasoline'
    diesel = 'Diesel'
    electric = 'Electric'
    hybrid = 'Hybrid'
    natural_gas = 'Natural Gas'
    ethanol = 'Ethanol'


class Colors(StrEnum):
    white = 'White'
    black = 'Black'
    silver = 'Silver'
    gray = 'Gray'
    blue = 'Blue'
    brown = 'Brown'
    gold = 'Gold'
    bronze = 'Bronze'


class Categories(StrEnum):
    economy = 'Economy'
    compact = 'Compact'
    suv = 'SUV'
    crossover = 'Crossover'
    luxury = 'Luxury'
    sports = 'Sports'
    convertible = 'Convertible'
    minivan = 'Minivan'
    pickup_truck = 'Pickup Truck'
