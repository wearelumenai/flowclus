import time
from datetime import datetime, timedelta

import requests

GET_START_STOP = 'http://localhost:8080/points?start={}&stop={}'


def get_data(every=2):
    """
    A generator that fetch new chunks each 2 seconds
    """
    start = datetime.now() - timedelta(seconds=every)
    stop = datetime.now()
    yield from get_chunk(start, stop)
    while True:
        time.sleep(every)
        start = stop
        stop = datetime.now()
        yield from get_chunk(start, stop)


def get_chunk(start, stop):
    """
    Issue the GET queries that returns points between instants start and stop
    """
    query = GET_START_STOP.format(start.isoformat(), stop.isoformat())
    yield requests.get(query).json()