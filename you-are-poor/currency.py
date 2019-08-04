"""Decimal representations of currency"""
import enum
from typing import Union


class Rounding(enum.Enum):
    FLOOR = enum.auto()
    CEILING = enum.auto()
    DEFAULT = enum.auto()


def _round(x: float, decimal_place: int, direction: Rounding) -> float:
    """Round up to the nearest place

    x: value to be rounded up
    decimal_place: the place to which ``x`` will be rounded. ``0`` will round
                   to the nearest integer.
    direction: method of rounding
    return: the rounded value
    """
    if decimal_place < 0:
        raise ValueError("decimal_place must be greater than 0")

    if decimal_place == 0:
        round_check: float = round(x, None)
    else:
        round_check: float = round(x, decimal_place)

    if round_check != x:
        if direction == Rounding.FLOOR:
            return 


class UnitedStatesDollar:
    """Representations of USD and mathematic operations accounting for rounding"""
    def __init__(self, dollar_value: Union[float, int]):
        """Instantiate a dollar value

        ``float`` passed as the initial value are rounded using ``round`` to two decimal places.
        dollar_value: the value, in USD
        """
        self._dollars: float = round(dollar_value, 2)

    def __str__(self):
        return f"${self._dollars}"

    def divide(self, divisor: Union[float, int], round_direction: Rounding) -> float:
