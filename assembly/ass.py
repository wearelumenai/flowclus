import numpy as np
import ot


class Assembly:
    """
    Keep track of known points and coalesce new ones
    """
    def __init__(self):
        self.points = np.empty((0,))

    def coalesce(self, points):
        """
        Coalesce the given points to the known points and compute a mapping
        between them.
        :param points: new points
        :return: new to known points mappings
        """
        if len(self.points) == 0:
            self.points = np.copy(points)
            return np.arange(len(points))
        elif len(points) > len(self.points):
            labels = self._match_longer(points)
            self.points = points[np.argsort(labels)]
            return labels
        else:
            labels = self._match_shorter(points)
            self.points[labels] = points
            return labels

    def _match_longer(self, longer):
        """compute mapping if new points are more than known points"""
        M, closest, farthest = _dist_closest(longer, self.points)
        G = ot.emd([], [], M[closest])
        result = np.empty((len(longer, )), dtype=int)
        result[closest] = np.argmax(G, axis=1)
        result[farthest] = np.arange(len(self.points), len(longer))
        return result

    def _match_shorter(self, shorter):
        """compute mapping if new points are less than known points"""
        M, known, _ = _dist_closest(self.points, shorter)
        G = ot.emd([], [], M[known])
        result = np.empty((len(shorter, )), dtype=int)
        result[np.argmax(G, axis=1)] = known
        return result


def _dist_closest(longer, shorter):
    """compute distance matrix, closest and farthest points"""
    M = ot.dist(longer, shorter)
    d = np.amin(M, axis=1)
    s = np.argsort(d)
    i = np.split(s, [len(shorter)])
    return M, i[0], i[1]
