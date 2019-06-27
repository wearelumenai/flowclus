import requests

GET_START_STOP = 'http://{}:{}/points?start={}&stop={}'


def get_chunk(host='localhost', port=8080):
    """
    Issue the GET queries that returns points between instants start and stop
    """

    def _(start, stop):
        query = GET_START_STOP.format(
            host, port, start.isoformat(), stop.isoformat()
        )
        chunk = requests.get(query).json()
        yield chunk['points'], chunk['columns']

    return _
