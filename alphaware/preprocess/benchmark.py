# -*- coding: utf-8 -*-

from collections import defaultdict
from toolz.dicttoolz import merge
from PyFin.Utilities import pyFinAssert
import pandas as pd
from argcheck import expect_types
from ..enums import (FreqType,
                     OutputDataFormat)
from ..utils import (convert_df_format,
                     ensure_datetime,
                     ensure_pd_index_names)
from ..const import (BENCHMARK_DATA,
                     MULTI_INDEX_FACTOR,
                     MULTI_INDEX_INDUSTRY_WEIGHT)

_REQUIRED_BENCHMARK_PROPERTY = {'data_format': OutputDataFormat.MULTI_INDEX_DF,
                                'freq': FreqType.EOM}


class Benchmark(object):
    @expect_types(data=BENCHMARK_DATA)
    def __init__(self, name, data, property_dict=defaultdict(str), **kwargs):
        self.name = name
        self.data = data
        self.property = merge(_REQUIRED_BENCHMARK_PROPERTY, property_dict)
        self.production_data_format = kwargs.get('production_data_format', OutputDataFormat.MULTI_INDEX_DF)
        self.hist_return = data.hist_return
        self.industry_weight = data.industry_weight  # 对标指数的行业成分比例

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
        date_index = self.data.index.get_level_values(multi_index.date_index)
        date_index = [ensure_datetime(date_, date_format) for date_ in date_index]
        data.reset_index(inplace=True)
        data[multi_index.date_index] = date_index
        if self.production_data_format == OutputDataFormat.MULTI_INDEX_DF:
            data.set_index(keys=multi_index.full_index, inplace=True)
        else:
            data.set_index(keys=multi_index.date_index, inplace=True)
        return

    def _validate_date_format(self):
        self._ensure_date_format(self.hist_return, MULTI_INDEX_FACTOR)
        self._ensure_date_format(self.industry_weight, MULTI_INDEX_INDUSTRY_WEIGHT)

    def get_industry_weight_on_date(self, date):
        pyFinAssert(self.industry_weight is not None, ValueError, 'industry weight data is empty')
        data = self.industry_weight.loc[date]
        data = data.reset_index().set_index(MULTI_INDEX_INDUSTRY_WEIGHT.industry_index)
        data = data.drop([MULTI_INDEX_INDUSTRY_WEIGHT.date_index], axis=1)
        data.loc['other'] = max(100 - data.sum(), 0)
        return data
