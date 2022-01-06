import json
import logging
import threading
import controller
import job_queue

connection = job_queue.connection
benchmark_queue = job_queue.Queue()


class BenchmarkConsumer:
    connection = job_queue.connection
    queue = job_queue.Queue()

    def __init__(self):
        self.consumer = self.connection.pubsub()
        for channel in ['benchmark_new', 'benchmark_done']:
            self.consumer.subscribe(channel)

    def run(self):
        """Runs the consumer."""

        # Listen for new messages and action.
        for message in self.consumer.listen():
            if message['type'] != 'message':
                continue
            try:
                data = json.loads(message['data'] or b'{}')
            except json.JSONDecodeError:
                logging.error(
                    'Could not decode message: {}'.format(message['data'])
                )
                continue

            fn = getattr(self, message['channel'].decode('utf-8'), None)
            if fn is None:
                logging.error(
                    'Could not find method for channel: {}'.format(
                        message['channel']
                    )
                )
                continue

            try:
                t = threading.Thread(target=fn, kwargs=data)
                t.start()
            except Exception as e:
                logging.error(
                    'Could not run thread for channel: {}'.format(
                        message['channel']
                    )
                )
                logging.error(e)

    def benchmark_new(
        self,
        benchmark_id: int,
        domain: str,
        num_servers: int,
        num_requests: int
    ) -> None:
        """Processes messages received via the `benchmark_new` channel.
        The method will add a benchmark to the queue and run if it is possible.

        Args:
            benchmark_id: The ID of the benchmark.
            domain: The domain to benchmark.
            num_servers: The number of servers to use.
            num_requests: The number of requests to run per server.
        """
        self.queue.push(benchmark_id, domain, num_servers, num_requests)
        self.run_next_job()

    def benchmark_done(self, num_servers: int) -> None:
        """Processes messages received via the `benchmark_done` channel.
        Releases the number of active nodes and runs the next benchmark in the
        queue.

        Args:
            num_servers: The number of servers that can be released back into
                the pool.
        """
        self.queue.remove_active_nodes(num_servers)
        self.run_next_job()

    def run_next_job(self):
        """Runs the next benchmark in the queue."""
        if not self.queue.can_run_next_job():
            return
        next_job = self.queue.pop()
        controller.run_benchmark(
            next_job['benchmark_id'],
            next_job['domain'],
            next_job['num_servers'],
            next_job['num_requests']
        )


if __name__ == '__main__':
    BenchmarkConsumer().run()
