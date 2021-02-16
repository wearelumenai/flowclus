from datetime import timedelta, datetime
from itertools import chain
from random import Random

from sklearn.datasets import make_blobs

def simulate(start, stop):
    start_minute = start.replace(second=0, microsecond=0)
    events = chain(simulate_minutes(start_minute, stop))
    return (ev for ev in events if start < ev['ts'] <= stop)

def simulate_minutes(start_minute, stop):
    while start_minute < stop:
        yield from simulate_minute(start_minute)
        start_minute += timedelta(minutes=1)

def simulate_minute(start_minute):
    # Generate the timestamps
    gen = Random()
    gen.seed(unix(start_minute))
    n = gen.randint(280, 320)
    timestamps = [start_minute + timedelta(seconds=gen.uniform(0, 60)) for _ in range(n)]

    # Generate the data points
    X, y = make_blobs(n_samples=n, centers=5, n_features=2, cluster_std=1)
    value = ({"X1": float(X[k,0]), "X2": float(X[k,1]), "label": int(y[k])} for k in range(len(X)))

    events = ({"ts": timestamps[k], "value": val} for k, val in enumerate(value))
    return sorted(events, key=lambda event: event['ts'])

def unix(ts):
    return (ts - datetime(1970, 1, 1)).total_seconds()
