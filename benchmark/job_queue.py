import os
import redis
import json


connection = redis.Redis(
    host=os.environ.get('EVENT_BUS_HOST', 'localhost'),
    port=os.environ.get('EVENT_BUS_PORT', 6379),
    db=os.environ.get('EVENT_BUS_DB', 0),
)

MAX_NODES = 32


class Queue:
    """A simple queue which ensures that the benchmarks are ran one at time.
    """

    def __init__(self, max_nodes: int = MAX_NODES, **kwargs):
        """Initializes the queue."""
        self.max_nodes = max_nodes
        if kwargs.pop('test', False):
            self.queue_name = 'benchmark.queue.test'
            self.nodes_count_name = 'benchmark.active_nodes_count.test'
        else:
            self.queue_name = 'benchmark.queue'
            self.nodes_count_name = 'benchmark.active_nodes_count'

    def __len__(self):
        """Returns the size of the queue."""
        return self.size()

    def __bool__(self):
        """Returns True if the queue is is_empty."""
        return not self.is_empty()

    def __iter__(self):
        """Iterates over the queue."""
        while not self.is_empty():
            yield self.pop()

    def __str__(self):
        """Returns a string representation of the queue."""
        return 'Queue({})'.format(self.size())

    def push(
        self,
        benchmark_id: int,
        url: str,
        num_nodes: int,
        requests_per_node: int
    ):
        """Pushes a new benchmark to the queue."""

        connection.rpush(
            self.queue_name,
            json.dumps({
                'benchmark_id': benchmark_id,
                'domain': url,
                'num_servers': num_nodes,
                'num_requests': requests_per_node
            })
        )

    def pop(self):
        """Pops a benchmark from the queue."""
        job = json.loads(connection.lpop(self.queue_name))
        self.add_active_nodes(job['num_servers'])
        return job

    def size(self):
        """Returns the size of the queue."""
        return connection.llen(self.queue_name)

    def is_empty(self):
        """Returns True if the queue is empty."""
        return self.size() == 0

    def clear(self):
        """Clears the queue."""
        connection.delete(self.queue_name)
        connection.delete(self.nodes_count_name)

    def active_nodes(self) -> int:
        """Returns the number of active nodes."""
        nodes = connection.get(self.nodes_count_name)
        if nodes is None:
            connection.set(self.nodes_count_name, 0)
            return 0
        return int(nodes)

    def add_active_nodes(self, num_nodes: int):
        """Adds the number of active nodes."""
        connection.incrby(self.nodes_count_name, num_nodes)

    def remove_active_nodes(self, num_nodes: int):
        """Removes the number of active nodes."""
        connection.decrby(self.nodes_count_name, num_nodes)

    def available_nodes(self) -> int:
        """Returns the number of available nodes."""
        return self.max_nodes - self.active_nodes()

    def can_run_next_job(self) -> bool:
        """Returns True if the next benchmark can be run."""
        next_job = connection.lindex(self.queue_name, 0)
        if next_job is None:
            return False
        next_job = json.loads(next_job)
        return self.available_nodes() >= next_job['num_servers']
