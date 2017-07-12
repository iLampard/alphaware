# -*- coding: utf-8 -*-


from sklearn.base import BaseEstimator
from abc import (ABCMeta,
                 abstractmethod)


class FactorEstimator(BaseEstimator):
    __metaclass__ = ABCMeta

    def fit(self, factor_container, **kwargs):
        return

    @abstractmethod
    def estimate(self, factor_container):
        return
