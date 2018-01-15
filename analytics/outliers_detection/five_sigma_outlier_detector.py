import numpy as np
from .abstract_outlier_detector import abstract_outlier_detector

class five_sigma_outlier_detector(abstract_outlier_detector):

    name = '5-sigma'

    def detect(self, data_frame, **kwargs):

        allMean, allSigma = np.mean(data_frame), np.std(data_frame)

        constraint = 5 * allSigma

        outlier = list(map(lambda x: x if abs(x - allMean) > constraint else None, data_frame))
        return outlier
