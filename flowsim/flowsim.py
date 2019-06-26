from datetime import timedelta, datetime
from itertools import chain
from random import Random


def _make_event(start, seconds, gen):
    return {
        'ts': start + timedelta(seconds=gen.uniform(0, seconds)),
        'value': draw_value(gen)
    }


def draw_value(gen):
    lorem = draw_mix([(3, 5), (6, 9)], [.5, .5], gen)
    ipsum = draw_mix([(5, 6), (7, 9)], [.6, .4], gen)
    dolor = draw_mix([(0, 4), (1, 5)], [.3, .7], gen)
    return {
        'lorem': gen.uniform(*lorem),
        'ipsum': gen.uniform(*ipsum),
        'dolor': gen.uniform(*dolor),
    }


def draw_mix(values, probas, gen):
    r = gen.uniform(0, 1)
    a = 0
    for v, p in zip(values, probas):
        a += p
        if a > r:
            return v


def simulate(start, stop):
    start_minute = start.replace(second=0, microsecond=0)
    events = chain(simulate_minutes(start_minute, stop))
    return (ev for ev in events if start < ev['ts'] <= stop)


def simulate_minutes(start_minute, stop):
    while start_minute < stop:
        yield from simulate_minute(start_minute)
        start_minute += timedelta(minutes=1)


def simulate_minute(start):
    gen = Random()
    gen.seed(unix(start))
    n = gen.randint(280, 320)
    events = (_make_event(start, 60, gen) for _ in range(n))
    return sorted(events, key=lambda event: event['ts'])


def unix(ts):
    return (ts - datetime(1970, 1, 1)).total_seconds()
