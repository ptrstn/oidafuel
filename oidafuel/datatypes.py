from enum import Enum


class FuelType(str, Enum):
    DIESEL = "DIE"
    SUPER_95 = "SUP"
    CNG_ERDGAS = "GAS"


class RegionType(str, Enum):
    BUNDESLAND = "BL"
    PB = "PB"
