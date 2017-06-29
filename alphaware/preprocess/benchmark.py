# -*- coding: utf-8 -*-

from collections import defaultdict
from toolz.dicttoolz import merge
from PyFin.Utilities import pyFinAssert
import numpy as np
from ..enums import (FreqType,
                     OutputDataFormat)
from ..utils import (convert_df_format,
                     ensure_datetime,
                     ensure_pd_index_names)
from ..const import (INDEX_FACTOR,
                     INDEX_INDUSTRY_WEIGHT)

_REQUIRED_BENCHMARK_PROPERTY = {'data_format': OutputDataFormat.MULTI_INDEX_DF,
                                'freq': FreqType.EOM}


class Benchmark(object):
    def __init__(self, name, hist_return=None, industry_weight=None, property_dict=defaultdict(str), **kwargs):
        self.name = name
        self.property = merge(_REQUIRED_BENCHMARK_PROPERTY, property_dict)
        self.production_data_format = kwargs.get('production_data_format', OutputDataFormat.MULTI_INDEX_DF)
        self.hist_return = hist_return
        self.industry_weight = industry_weight  # 对标指数的行业成分比例

        self._validate_data_format()
        self._validate_date_format()

    def _ensure_data_format(self, data):
        if self.property['data_format'] != self.production_data_format:
            if data is not None:
                data = convert_df_format(data, target_format=self.production_data_format)
        return

    def _validate_data_format(self):
        self._ensure_data_format(self.hist_return)
        self._ensure_data_format(self.industry_weight)

    def _ensure_date_format(self, data, multi_index):
        date_format = self.property.get('date_format', '%Y-%m-%d')
        data = ensure_pd_index_names(data, data_format=self.production_data_format, valid_index=multi_index)
        date_index = data.index.get_level_values(multi_index.date_index)
        date_index = [ensure_datetime(date_, date_format) for date_ in date_index]
        data.reset_index(inplace=True)
        data[multi_index.date_index] = date_index
        if self.production_data_format == OutputDataFormat.MULTI_INDEX_DF:
            data.set_index(keys=multi_index.full_index, inplace=True)
            if hasattr(multi_index, 'col_name'):
                data.columns = multi_index.col_name
        else:
            data.set_index(keys=multi_index.date_index, inplace=True)
        return

    def _validate_date_format(self):
        self._ensure_date_format(self.hist_return, INDEX_FACTOR)
        self._ensure_date_format(self.industry_weight, INDEX_INDUSTRY_WEIGHT)

    def get_industry_weight_on_date(self, date):
        pyFinAssert(self.industry_weight is not None, ValueError, 'industry weight data is empty')
        date = ensure_datetime(date)
        data = self.industry_weight.loc[date]
        data = data.reset_index().set_index(INDEX_INDUSTRY_WEIGHT.industry_index)
        data = data[data.columns[0]]
        resid_weight = 100 - np.sum(data.values)
        data['other'] = resid_weight if resid_weight > 0 else 0.0
        return data
