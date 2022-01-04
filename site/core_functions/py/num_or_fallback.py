"""Will attempt to convert a provided value into an number.
If this causes an error then set the return value a fallback value that
would be expected as an argument.
"""


def num_or_fallback(value, fallback, type='F'):
    """Attempts to convert an ``value`` into a number. If this fails, then
    return the ``fallback``.

    Args:
        * value (any): The value to be converted to a number.
        * fallback (any): Fallback value should the conversion fail.
        * type (str ['F'|'I']): Define what type of number to return the value
            as. F=float, I=integer.
    """
    try:
        if type == 'F':
            return float(value)
        elif type == 'I':
            return int(value)
        else:
            raise ValueError(
                "Invalid argument for ``type``. F=float, I=integer."
            )

    except (ValueError, TypeError):
        return fallback
