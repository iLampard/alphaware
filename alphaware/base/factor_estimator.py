# -*- coding: utf-8 -*-


from sklearn.base import BaseEstimator
from argcheck import (preprocess,
                      expect_types)
from .factor_container import ensure_factor_container


class FactorEstimator(BaseEstimator):
    def __init__(self):
        self.df_mapper = None

    @expect_types(out=bool)
    def set_out_container(self, out):
        self.out_container = out

    @preprocess(factor_container=ensure_factor_container)
    def fit(self, factor_container, **kwargs):
        self.df_mapper = self._build_mapper(factor_container)
        return self

    def _build_mapper(self, factor_container):
        raise NotImplementedError

    @preprocess(factor_container=ensure_factor_container)
    def estimate(self, factor_container):
        return factor_container.data
