# -*- coding: utf-8 -*-

import copy
import pandas as pd
import numpy as np
from collections import defaultdict
from toolz.dicttoolz import (merge,
                             dissoc)
from PyFin.Utilities import pyFinAssert
from argcheck import expect_types
from ..utils import (FreqType,
                     FactorType,
                     OutputDataFormat,
                     FactorNormType,
                     ensure_pyfin_date,
                     MULTI_INDEX_NAMES,
                     convert_df_format)

_REQUIRED_FACTOR_PROPERTY = {'type': FactorType.ALPHA_FACTOR,
                             'data_format': OutputDataFormat.MULTI_INDEX_DF,
                             'norm_type': FactorNormType.Null,
                             'freq': FreqType.EOM}


@expect_types(factor_property=dict)
def update_factor_property(factor_property):
    ret = merge(_REQUIRED_FACTOR_PROPERTY, factor_property)
    return ret


class Factor(object):
    def __init__(self, data, name, property_dict=defaultdict(str), **kwargs):
        self.data = copy.deepcopy(data)
        self.name = name
        self.property = update_factor_property(property_dict)
        self.date_index_name = kwargs.get('date_index_name', MULTI_INDEX_NAMES[0])
        self.sec_index_name = kwargs.get('sec_index_name', MULTI_INDEX_NAMES[1])
        self.target_data_format = kwargs.get('target_data_format', OutputDataFormat.MULTI_INDEX_DF)

        self._validate_data_format()
        self._validate_data_name()
        self._validate_date_index()

    def _validate_date_index(self):
        date_format = self.property.get('date_format', '%Y-%m-%d')
        date_index = self.data.index.get_level_values(self.date_index_name)
        date_index = [ensure_pyfin_date(date_, date_format).toDateTime() for date_ in date_index]
        self.data.reset_index(inplace=True)
        self.data[self.date_index_name] = date_index
        self.data.set_index(keys=MULTI_INDEX_NAMES, inplace=True)

    @property
    def factor_type(self):
        return self.property['type']

    def _validate_data_format(self):
        if self.property['data_format'] != self.target_data_format:
            self.data = convert_df_format(self.data, target_format=self.target_data_format)

        return

    def _validate_data_name(self):
        self.data.columns = [self.name]

    def get_unique_date_list(self):
        if self.property['data_format'] == OutputDataFormat.MULTI_INDEX_DF:
            ret = set(self.data.index.get_level_values(self.date_index_name))
        else:
            ret = self.data.index
        return sorted(set(ret))
