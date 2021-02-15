from collections import deque

import numpy as np
from distclus import Batch, MCMC

from assembly import Assembly


class OC:
    """Wraps a mini batch MCMC algorithm"""
    def __init__(self, **kwargs):
        """
        Build a new OC instance
        """
        frame_size = kwargs.get('frame_size', 100)
        self.frame = deque([], frame_size)
        del kwargs['frame_size']
        self.algo = Batch(MCMC, **kwargs)
        self.ass = Assembly()

    def push_predict(self, points, columns):
        """
        push and predict data from the dataflow
        :param points: a chunk of data
        :param columns: the column names
        :return: the result that can be send to the dataviz server
        """
        arr = self._extend(points)
        self.algo.push(arr)
        centroids, labels = self.algo.predict(arr)
        return self._make_result(centroids, labels, columns)

    def _extend(self, points):
        """
        keep the given chunk in the fixed size frame. Old data can be reused
        if the chunk is smaller than the frame.
        :param points: a chunk of data
        :return: the content of the frame as a ndarray
        """
        self.frame.extend(points)
        return np.array(self.frame)

    def _make_result(self, centroids, labels, columns):
        """
        Build a result ready for the dataviz server. The result contains
        all known centers, even if empty for the current centroids
        :param centroids: the current centroids
        :param labels: the labels for the data in the frame
        :param columns: the column names
        :return: the result ready fo the dataviz server
        """
        indices = self.ass.coalesce(centroids)
        counts = np.zeros(len(self.ass.points))
        counts[indices] = np.bincount(labels)
        return {
            'centers': self.ass.points.tolist(),
            'counts': counts.tolist(),
            'columns': columns
        }

    def run(self):
        """Run the underlying algorithm"""
        return self.algo.run()
