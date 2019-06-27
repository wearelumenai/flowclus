import time
from datetime import datetime, timedelta

from bubbles import Server
from bubbles.singletondriver import SingletonDriver


def start_server(host='localhost', port=8081, result_id='batch_tutorial'):
    """
    Starts the dataviz server
    :param host: the host that the server listens for
    :param port: the port that the server listens on
    :param result_id: the identifier used to store and get the results
    :return: a SingletonDriver that backends the server
    """
    driver = SingletonDriver(result_id)
    server = Server(driver)
    server.start(host=host, port=port, quiet=True)
    print('visit http://{}:{}/bubbles?result_id={}'.format(
        host, port, result_id
    ))
    return driver


def run(model, get_chunk, driver, every=2):
    """
    Run the clustering and dataviz server
    :param model: the OC instance that manage cluster computing
    :param get_chunk: a method that takes two instants and returns
    points between them
    :param driver: the SingletonDriver that stores the results
    :param every: polling time
    """
    with model.run():
        for points, columns in get_data(get_chunk, every):
            result = model.push_predict(points, columns)
            driver.put_result(result)


def get_data(get_chunk, every):
    """
    A generator that fetch new chunks each 2 seconds
    :param get_chunk: a method that takes two instants and returns
    points between them
    :param every: polling time
    :return: a generator of (points, column names) tuples
    """
    start = datetime.now() - timedelta(seconds=every)
    stop = datetime.now()
    yield from get_chunk(start, stop)
    while True:
        time.sleep(every)
        start = stop
        stop = datetime.now()
        yield from get_chunk(start, stop)
