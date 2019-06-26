import numpy as np
import ot


class Assembly:
    def __init__(self):
        self.points = np.empty((0,))

    def coalesce(self, points):
        if len(self.points) == 0:
            self.points = np.copy(points)
            return np.arange(len(points))
        elif len(points) > len(self.points):
            labels = match_longer(self.points, points)
            self.points = points[np.argsort(labels)]
            return labels
        else:
            labels = match_shorter(self.points, points)
            self.points[labels] = points
            return labels


def match_longer(shorter, longer):
    M, closest, farthest = dist_closest(longer, shorter)
    G = ot.emd([], [], M[closest])
    result = np.empty((len(longer, )), dtype=int)
    result[closest] = np.argmax(G, axis=1)
    result[farthest] = np.arange(len(shorter), len(longer))
    return result


def match_shorter(longer, shorter):
    M, known, _ = dist_closest(longer, shorter)
    G = ot.emd([], [], M[known])
    result = np.empty((len(shorter, )), dtype=int)
    result[np.argmax(G, axis=1)] = known
    return result


def dist_closest(longer, shorter):
    M = ot.dist(longer, shorter)
    d = np.amin(M, axis=1)
    s = np.argsort(d)
    i = np.split(s, [len(shorter)])
    return M, i[0], i[1]
