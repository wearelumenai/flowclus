import json
from datetime import datetime, timedelta

import bottle

try:
    from flowsim.flowsim_sklearn import simulate, unix
except:
    from flowsim.flowsim import simulate, unix


@bottle.route('/points')
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
    if param in bottle.request.query:
        stop = datetime.strptime(bottle.request.query[param]
                                 , '%Y-%m-%dT%H:%M:%S.%f')
    else:
        stop = default
    return stop


def run(host='localhost', port='8080', quiet=True):
    bottle.run(host=host, port=port, quiet=quiet)
