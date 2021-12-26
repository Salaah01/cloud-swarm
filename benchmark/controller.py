"""This module relates to the main controller for managing the various nodes
needed to benchmark a site.
"""

import typing as _t
import os
import subprocess
import threading
import time
from datetime import datetime, timedelta
try:
    from . import ec2
except ImportError:
    import ec2


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class SlaveNode:
    """Represents a node that is used to carry out a benchmark."""

    def __init__(self, instance):
        """Creates a slave node.
        Args:
            instance (boto3.resources.ec2.Instance): Instance to use
        """
        self.instance = instance
        self.host = instance.public_ip_address

    def schedule_benchmark(self, ts: datetime, num_requests: int, url: str):
        """Schedules a benchmark on the node.
        Args:
            ts (datetime): Time to start the benchmark
            num_requests (int): Number of requests to run
            url (str): URL to benchmark
        """
        subprocess.call([
            os.path.join(BASE_DIR, 'benchmark_setup.sh'),
            self.host,
            ts.strftime('%m%d%H%M'),
            str(num_requests),
            url
        ])

    def benchmark_results(self):
        """Returns the results of the benchmark."""
        subprocess.call([
            os.path.join(BASE_DIR, 'benchmark_results.sh'),
            self.host
        ])


class MasterNode:
    """Master node responsible for managing all the slave nodes which would
    be responsible for running the benchmark.
    """

    def __init__(self, url: str, num_nodes: int = 1,
                 requests_per_node: int = 1,
                 instance_type: _t.Optional[str] = None,
                 key_name: _t.Optional[str] = None):
        """Creates a master node.
        Args:
            url (str): URL of the site to benchmark
            num_nodes (int): Number of nodes to create
            requests_per_node (int): Number of requests to run per node
            instance_type (str): Instance type to create
            key_name (str): Key name to use
        """
        self.url = url
        self.num_nodes = num_nodes
        self.requests_per_node = requests_per_node
        self.instance_type = instance_type
        self.key_name = key_name

        self.nodes: _t.List[SlaveNode] = []

    def __enter__(self):
        """Enters the context manager."""
        self.spawn_nodes()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exits the context manager."""
        self.terminate_nodes()

    def __iter__(self):
        """Iterates over the nodes."""
        return iter(self.nodes)

    def __len__(self):
        """Returns the number of nodes."""
        return len(self.nodes)

    def instances(self) -> _t.List:
        """Returns the list of instances."""
        return [node.instance for node in self.nodes]

    def spawn_nodes(self) -> None:
        """Spawns a collection of nodes."""
        instances = ec2.create_instances(num_instances=self.num_nodes)
        for instance in instances:
            self.nodes.append(SlaveNode(instance))

    def terminate_nodes(self) -> None:
        """Terminates all the nodes."""
        ec2.terminate_instances(self.instances())
        self.nodes = []

    def benchmark_start_ts(self) -> datetime:
        """Lazy getter for when the benchmark run should start."""
        if not hasattr(self, '_benchmark_start_ts'):
            # Assume that it takes 1.5 seconds to schedule the benchmark.
            ms_to_setup = 1500
            self._benchmark_start_ts = datetime.now() + timedelta(
                milliseconds=len(self.nodes) * ms_to_setup
            )
        return self._benchmark_start_ts

    def execute_tasks(self) -> None:
        """Executes a set of tasks on all node."""
        threads = []
        for node in self.nodes:
            t = threading.Thread(
                target=self.execute_tasks_on_node,
                args=(node,)
            )
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

    def execute_tasks_on_node(self, node) -> None:
        """Executes the tasks on a single node."""
        tasks = [
            self._execute_task_schedule_benchmark,
            self._execute_task_benchmark_results
        ]
        for task in tasks:
            task(node)

    def _execute_task_schedule_benchmark(self, node: SlaveNode) -> None:
        """Executes the task to schedule the benchmark."""
        node.schedule_benchmark(
            self.benchmark_start_ts(),
            self.requests_per_node,
            self.url
        )

    def _execute_task_benchmark_results(self, node: SlaveNode) -> None:
        """Executes the task to get the benchmark results.
        Args:
            node (SlaveNode): Node to execute the task on
        Returns:
            None
        """
        # Check that the benchmark has finished (base this on the scheduled
        # start time).
        if datetime.now() < self.benchmark_start_ts():
            sleep_time = self.benchmark_start_ts() - datetime.now()
            print(
                f'[{datetime.now().strftime("%H:%M")}] Results not ready, sleeping for {sleep_time}'
            )
            time.sleep(sleep_time.total_seconds())
        node.benchmark_results()


if __name__ == '__main__':
    master = MasterNode(num_nodes=2, requests_per_node=10)
    master.spawn_nodes()
    master.execute_tasks()
    master.terminate_nodes()
