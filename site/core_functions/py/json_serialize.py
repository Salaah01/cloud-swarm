"""Convert a collection of data into JSON."""

import datetime
import decimal


class JsonSerialize:
    """Convert a collection of data into JSON."""

    @staticmethod
    def makes_json_compatible(item):
        """Converts an ``item`` to a format which is compatible within a JSON
        object.
        Args:
            item: (any) Item to convert.
        """
        if isinstance(item, decimal.Decimal):
            return float(item)

        if isinstance(item, (datetime.date, datetime.datetime)):
            return str(item)

        return item

    @staticmethod
    def is_handled_collection(collection):
        """Checks if the ``collection`` provided is of a collection type that
        is handled by the class.
        Args:
            collection: (any) Collection of items to check.
        """
        return isinstance(collection, (list, tuple, dict))

    def json_serialize(self, data):
        """Convert a collection of data into JSON.
        Args:
            data: (list|tuple|dict) A collection of data to convert.
        """

        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                if self.is_handled_collection(value):
                    result[key] = self.json_serialize(value)
                else:
                    result[key] = self.makes_json_compatible(value)
            return result

        if isinstance(data, (list, tuple)):
            result = []
            for item in data:
                if self.is_handled_collection(item):
                    result.append(self.json_serialize(item))
                else:
                    result.append(self.makes_json_compatible(value))
            return result

        return self.makes_json_compatible(data)
