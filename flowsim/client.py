import requests

GET_START_STOP = 'http://localhost:8080/points?start={}&stop={}'


def get_chunk(start, stop):
    """
    Issue the GET queries that returns points between instants start and stop
    """
    query = GET_START_STOP.format(start.isoformat(), stop.isoformat())
    chunk = requests.get(query).json()
    yield chunk['points'], chunk['columns']