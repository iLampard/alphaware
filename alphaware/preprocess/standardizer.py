# -*- coding: utf-8 -*-


from sklearn_pandas import DataFrameMapper
from sklearn.preprocessing import StandardScaler
from .factor_transformer import FactorTransformer
from ..enums import FactorType


class FactorStandardizer(FactorTransformer):
    def __init__(self, copy=True, groupby_date=True, out_container=False, with_mean=True, with_std=True):
        super(FactorStandardizer, self).__init__(copy=copy, groupby_date=groupby_date, out_container=out_container)
        self.with_mean = with_mean
        self.with_std = with_std

    def _build_imputer_mapper(self, factor_container):
        data = factor_container.data
        data_mapper = [([factor_name], self._get_imputer(factor_container.property[factor_name]['type']))
                       for factor_name in data.columns]
        return DataFrameMapper(data_mapper)

    def _get_imputer(self, factor_type):
        if factor_type == FactorType.INDUSTY_CODE:
            return None
        elif factor_type == FactorType.ALPHA_FACTOR or factor_type == FactorType.RETURN:
            return StandardScaler(copy=self.copy, with_mean=self.with_mean, with_std=self.with_std)