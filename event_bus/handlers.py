"""Contains the handlers for the event bus."""


def benchmark_new(data: dict) -> None:
    """Handler for the 'benchmark_new' event."""
    print('benchmark_new:', data)
