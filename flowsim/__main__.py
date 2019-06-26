import json
from datetime import datetime, timedelta

from bottle import route, request, run

from .flowsim import simulate, unix


@route('/points')
def points():
    start = get_param('start', datetime.now() - timedelta(hours=1))
    stop = get_param('stop', datetime.now())
    ts = []
    points = []
    columns = None
    for ev in simulate(start, stop):
        ts.append(unix(ev['ts']))
        if columns is None:
            columns, point = get_point_with_columns(ev)
        else:
            point = get_point(ev, columns)
        points.append(point)

    return json.dumps({'ts': ts, 'points': points, 'columns': columns})


def get_point_with_columns(ev):
    point = []
    columns = []
    for name, value in ev['value'].items():
        columns.append(name)
        point.append(value)
    return columns, point


def get_point(ev, columns):
    point = []
    for name in columns:
        point.append(ev['value'][name])
    return point


def get_param(param, default):
    if param in request.query:
        stop = datetime.fromisoformat(request.query[param])
    else:
        stop = default
    return stop


if __name__ == "__main__":
    run(host='localhost')
