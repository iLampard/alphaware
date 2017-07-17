# -*- coding: utf-8 -*-


from sklearn.base import BaseEstimator
from abc import abstractmethod


class FactorEstimator(BaseEstimator):
    def fit(self, factor_container, **kwargs):
        return self

    @abstractmethod
    def predict(self, factor_container):
        return
