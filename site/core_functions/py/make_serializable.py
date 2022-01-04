"""Convert an array of data to a JSON serializable format."""

import decimal
import datetime


def make_serializable(dataArray):
    """Converts an array of data to a JSON serializable format.
    Args:
        dataArray: (list|tuple) An array of data to convert.
    """

    newArray = []

    for data in dataArray:
        if isinstance(data, decimal.Decimal):
            newArray.append(float(data))
            continue

        if (isinstance(data, datetime.date)
                or isinstance(data, datetime.datetime)):
            newArray.append(str(data))
            continue

        newArray.append(data)

    return newArray
