# -*- coding: utf-8 -*-

import pandas as pd
from argcheck import expect_types
from .enums import OutputDataFormat
from .const import MULTI_INDEX_NAMES


@expect_types(data=(pd.Series, pd.DataFrame))
def convert_df_format(data, target_format=OutputDataFormat.MULTI_INDEX_DF, col_name=list('factor'),
                      index_name=MULTI_INDEX_NAMES):
    if target_format == OutputDataFormat.MULTI_INDEX_DF:
        data_ = data.stack()
        data_ = pd.DataFrame(data_)
        data_.index.names = index_name
        data_.columns = col_name
    else:
        data_ = data.unstack()
        data_.reset_index(inplace=True)

    return data_
