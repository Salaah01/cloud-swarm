"""This module relates to the main controller for managing the various nodes
needed to benchmark a site.
"""

import typing as _t
import os
import subprocess
import threading
from datetime import datetime, timedelta
try:
    from . import ec2
except ImportError:
    import ec2


class SlaveNode:
    """Represents a node that is used to carry out a benchmark."""

    BENCHMARK_SETUP_SCRIPT = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'benchmark_setup.sh'
    )

    def __init__(self, instance):
        """Creates a slave node.
        Args:
            instance (boto3.resources.ec2.Instance): Instance to use
        """
        self.instance = instance

    def schedule_benchmark(self, ts: datetime, num_requests: int, url: str):
        """Schedules a benchmark on the node.
        Args:
            ts (datetime): Time to start the benchmark
            num_requests (int): Number of requests to run
            url (str): URL to benchmark
        """
        subprocess.call([
            self.BENCHMARK_SETUP_SCRIPT,
            self.instance.public_ip_address,
            ts.strftime('%m%d%H%M'),
            str(num_requests),
            url
        ])

    def results_benchmark(self):
        """Returns the results of the benchmark."""


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

    def execute_tasks(self) -> None:
        """Executes a set of tasks on all node."""
        threads = []
        for node in self.nodes:
            t = threading.Thread(
                target=self._execute_tasks_on_node,
                args=(node,)
            )
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

    def _execute_tasks_on_node(self, node) -> None:
        """Executes the tasks a node.
        Args:
            node (SlaveNode): Node to execute the task on
        Returns:
            None
        """
        tasks = [self._execute_task_schedule_benchmark]
        for task in tasks:
            task(node)

    def _execute_task_schedule_benchmark(self, node: SlaveNode) -> None:
        """Executes the task to schedule the benchmark.
        Args:
            node (SlaveNode): Node to execute the task on
        Returns:
            None
        """

        # Assume that it takes 1.5 seconds to schedule the benchmark.
        ms_to_setup = 1500

        schedule_at = datetime.now() + timedelta(
            milliseconds=len(self.nodes) * ms_to_setup
        )

        # Schedule the benchmark
        node.schedule_benchmark(
            schedule_at,
            self.requests_per_node,
            self.url
        )


if __name__ == '__main__':
    # with MasterNode(num_nodes=2, requests_per_node=10) as master:
    #     print(master.execute_tasks())
    master = MasterNode(num_nodes=2, requests_per_node=10)
    master.execute_tasks()
