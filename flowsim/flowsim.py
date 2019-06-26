from datetime import timedelta, datetime
from itertools import chain
from random import randint, uniform, seed, Random


def _make_event(start, gen):
    return {
        'ts': start + timedelta(minutes=gen.uniform(0, 60)),
        'value': draw_value(gen)
    }


def draw_value(gen):
    lorem = draw_mix([1, 10], [.5, .5], gen)
    ipsum = draw_mix([1, 6], [.6, .4], gen)
    dolor = draw_mix([2, 5], [.3, .7], gen)
    sit = draw_mix([5, 11], [.5, .5], gen)
    amet = draw_mix([15, 17], [.5, .5], gen)
    consectetur = draw_mix([1, 12], [.5, .5], gen)
    return {
        'lorem': gen.uniform(0, lorem),
        'ipsum': gen.uniform(0, ipsum),
        'dolor': gen.uniform(0, dolor),
        'sit': gen.uniform(0, sit),
        'amet': gen.uniform(0, amet),
        'consectetur': gen.uniform(0, consectetur)
    }


def draw_mix(values, probas, gen):
    r = gen.uniform(0, 1)
    a = 0
    for v, p in zip(values, probas):
        a += p
        if a > r:
            return v


def simulate(start, stop):
    start_hour = start.replace(minute=0, second=0, microsecond=0)
    events = chain(simulate_hours(start_hour, stop))
    return (ev for ev in events if start <= ev['ts'] <= stop)


def simulate_hours(start_hour, stop):
    while start_hour < stop:
        yield from simulate_hour(start_hour)
        start_hour += timedelta(hours=1)


def simulate_hour(start):
    gen = Random()
    gen.seed(unix(start))
    n = gen.randint(12, 15)
    events = (_make_event(start, gen) for _ in range(n))
    return sorted(events, key=lambda event: event['ts'])


def unix(ts):
    return (ts - datetime(1970, 1, 1)).total_seconds()
