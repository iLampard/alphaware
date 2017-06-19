# -*- coding: utf-8 -*-

import numpy as np
from sklearn_pandas import DataFrameMapper
from sklearn.base import (BaseEstimator,
                          TransformerMixin)
from sklearn.linear_model import LinearRegression
from .factor_estimator import FactorEstimator
from ..enums import (FactorType,
                     FactorNormType)


def get_indicator_matrix(industry_code, mkt_cap=None):
    """
    :return: np.matrix, 行业虚拟矩阵，see alphaNote
    """
    nb_sec_id = len(industry_code)
    unique_industry = np.unique(industry_code)
    nb_unique_industry = len(unique_industry)
    ret = np.zeros((nb_sec_id, nb_unique_industry))
    for i in range(nb_sec_id):
        col_index = np.where(unique_industry == industry_code[i])[0]
        ret[i][col_index] = 1.0
    if mkt_cap is not None:
        array_cap = mkt_cap.reshape(mkt_cap.shape[0], 1)
        # 合并两个矩阵构成大矩阵
        ret = np.hstack((ret, array_cap))

    return ret


class Neutralizer(BaseEstimator, TransformerMixin):
    def __init__(self, industry, mkt_cap=None):
        self.industry = industry
        self.mkt_cap = mkt_cap

    def fit(self):
        return self

    def transform(self, x):
        if self.mkt_cap is not None:
            lcap_ = np.log(self.mkt_cap)
        else:
            lcap_ = None

        Y = x.values.reshape(-1, 1)
        X = get_indicator_matrix(self.industry, lcap_)
        linreg = LinearRegression(fit_intercept=False)
        model = linreg.fit(X, Y)
        coef = np.mat(linreg.coef_)
        a = np.dot(X, coef.T)
        residues = Y - a

        return np.asmatrix(residues).A1


class FactorNeutralizer(FactorEstimator):
    def __init__(self, copy=True, groupby_date=True):
        super(FactorNeutralizer, self).__init__(copy=copy, groupby_date=groupby_date)

    def _build_imputer_mapper(self, factor_container):
        data = factor_container.data
        industry_code = factor_container.industry_code
        mkt_cap = factor_container.mkt_cap
        data_mapper = [([factor_name],
                        self._get_imputer(factor_type=factor_container.property[factor_name]['type'],
                                          factor_norm_type=factor_container.property[factor_name]['norm_type'],
                                          industry_code=industry_code,
                                          mkt_cap=mkt_cap))
                       for factor_name in data.columns]
        return DataFrameMapper(data_mapper)

    def _get_imputer(self, factor_type, factor_norm_type, industry_code, mkt_cap=None):
        if factor_type == FactorType.INDUSTY_CODE or factor_norm_type == FactorNormType.Null:
            return None
        elif factor_type == FactorType.ALPHA_FACTOR or factor_type == FactorType.RETURN:
            if factor_norm_type == FactorNormType.Industry_Cap_Neutral:
                return Neutralizer(industry_code)
            else:
                return Neutralizer(industry_code, mkt_cap)
