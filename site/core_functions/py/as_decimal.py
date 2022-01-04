from typing import Union
from decimal import Decimal


def as_2dp_decimal(value: Union[int, float, Decimal]) -> Decimal:
    """Converts a float to a 2.dp decimal handling any floating point errors.
    """
    return Decimal('{:.2f}'.format(value))
