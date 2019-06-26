import json
from datetime import datetime, timedelta

from bottle import route, request, run

from .flowsim import simulate, unix


@route('/points')
def points():
    start = request.query.get('start', datetime.now() - timedelta(days=1))
    stop = request.query.get('stop', datetime.now())
    events = [{'ts': unix(ev['ts']), 'value': ev['value']}
              for ev in simulate(start, stop)]
    return json.dumps(events)


if __name__ == "__main__":
    run(host='localhost')
