# -*- coding: utf-8 -*-

import pandas as pd
from argcheck import expect_types
from alphaware.const import INDEX_FACTOR
from alphaware.enums import OutputDataFormat


@expect_types(data=(pd.Series, pd.DataFrame))
def convert_df_format(data, target_format=OutputDataFormat.MULTI_INDEX_DF, col_name='factor',
                      multi_index=INDEX_FACTOR):
    if target_format == OutputDataFormat.MULTI_INDEX_DF:
        tmp = data.stack()
        data_ = pd.DataFrame(tmp)
        data_.index.names = multi_index.full_index
        data_.columns = [col_name]
    else:
        tmp = data.unstack()
        index = tmp.index
        columns = tmp.columns.get_level_values(multi_index.sec_index).tolist()
        data_ = pd.DataFrame(tmp.values, index=index, columns=columns)

    return data_
