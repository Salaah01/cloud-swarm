import os
import redis
import json
import logging
import threading
import controller

connection = redis.Redis(
    host=os.environ.get('EVENT_BUS_HOST', 'localhost'),
    port=os.environ.get('EVENT_BUS_PORT', 6379),
    db=os.environ.get('EVENT_BUS_DB', 0),
)


def new_benchmark_consumer():
    """Listens for new benchmark requests and calls the appropriate handler."""

    consumer = connection.pubsub()

    # Subscribe to each channel.
    consumer.subscribe('benchmark.new')

    # Listen for messages.
    for message in consumer.listen():
        if message['type'] != 'message':
            continue
        data = json.loads(message['data'])
        try:
            t = threading.Thread(
                target=controller.run_benchmark,
                kwargs={
                    'benchmark_id': data['benchmark_id'],
                    'url': data['domain'],
                    'num_nodes': data['num_servers'],
                    'requests_per_node': data['num_requests']
                }
            )
            t.start()
        except Exception as e:
            logging.error(e)


if __name__ == '__main__':
    new_benchmark_consumer()
