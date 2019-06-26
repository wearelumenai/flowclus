from collections import deque

import numpy as np
from distclus import Batch, MCMC

from assembly import Assembly


class OC:
    def __init__(self):
        self.ass = Assembly()
        self.algo = Batch(MCMC, init_k=1, b=1, amp=.2, mcmc_iter=100)
        self.frame = deque([], 60)

    def push_predict(self, chunk):
        arr = self._extend(chunk)
        self.algo.push(arr)
        centroids, labels = self.algo.predict_online(arr)
        return self._make_result(centroids, labels, chunk['columns'])

    def _extend(self, chunk):
        self.frame.extend(chunk['points'])
        return np.array(self.frame)

    def _make_result(self, centroids, labels, columns):
        indices = self.ass.coalesce(centroids)
        counts = np.zeros(len(self.ass.points))
        counts[indices] = np.bincount(labels)
        return {
            'centers': self.ass.points.tolist(),
            'counts': counts.tolist(),
            'columns': columns
        }

    def run(self):
        return self.algo.run()
