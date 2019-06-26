from bubbles import Server
from bubbles.singletondriver import SingletonDriver

from .data import get_data
from .oc import OC


def run():
    model = OC()
    driver = _start_server()
    with model.run():
        for chunk in get_data():
            result = model.push_predict(chunk)
            driver.put_result(result)


def _start_server():
    driver = SingletonDriver('batch_tutorial')
    server = Server(driver)
    server.start(port=8081, quiet=True)
    print('visit http://localhost:8081/bubbles?result_id=batch_tutorial')
    return driver


if __name__ == "__main__":
    run()
