# -*- coding: utf-8 -*-

import pandas as pd
from argcheck import expect_types
from alphaware.const import MULTI_INDEX_NAMES
from alphaware.enums import OutputDataFormat


@expect_types(data=(pd.Series, pd.DataFrame))
def convert_df_format(data, target_format=OutputDataFormat.MULTI_INDEX_DF, col_name=list('factor'),
                      index_name=MULTI_INDEX_NAMES):
    if target_format == OutputDataFormat.MULTI_INDEX_DF:
        tmp = data.stack()
        data_ = pd.DataFrame(tmp)
        data_.index.names = index_name
        data_.columns = col_name
    else:
        tmp = data.unstack()
        index = tmp.index
        columns = tmp.columns.get_level_values(MULTI_INDEX_NAMES[1]).tolist()
        data_ = pd.DataFrame(tmp.values, index=index, columns=columns)

    return data_
