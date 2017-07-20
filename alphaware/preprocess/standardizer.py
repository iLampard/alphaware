# -*- coding: utf-8 -*-


from sklearn.preprocessing import StandardScaler
from sklearn_pandas import DataFrameMapper
from ..base import FactorTransformer
from ..enums import FactorType


class FactorStandardizer(FactorTransformer):
    def __init__(self, copy=True, out_container=False, with_mean=True, with_std=True):
        super(FactorStandardizer, self).__init__(copy=copy, out_container=out_container)
        self.with_mean = with_mean
        self.with_std = with_std

    def _build_mapper(self, factor_container):
        data = factor_container.data
        data_mapper = [([factor_name], self._get_mapper(factor_container.property[factor_name]['type']))
                       for factor_name in data.columns]
        return DataFrameMapper(data_mapper)

    def _get_mapper(self, factor_type):
        if factor_type == FactorType.INDUSTY_CODE:
            return None
        else:
            return StandardScaler(copy=self.copy, with_mean=self.with_mean, with_std=self.with_std)