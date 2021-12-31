import os
import redis
import json
import logging
import handlers

connection = redis.Redis(
    host=os.environ.get('EVENT_BUS_HOST', 'localhost'),
    port=os.environ.get('EVENT_BUS_PORT', 6379),
    db=os.environ.get('EVENT_BUS_DB', 0),
)

channels = [
    'benchmark_new',
]


def manage_events():
    """Subscribed to all channels and dispatches events to the appropriate
    handler.
    """

    consumer = connection.pubsub()

    # Subscribe to each channel.
    for channel in channels:
        consumer.subscribe(channel)

    # Listen for messages.
    for message in consumer.listen():
        if message['type'] != 'message':
            continue
        data = json.loads(message['data'])
        try:
            getattr(handlers, message['channel'].decode('utf-8'))(data)
        except Exception as e:
            print(e)
            logging.error(e)


if __name__ == '__main__':
    manage_events()
