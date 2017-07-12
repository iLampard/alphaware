# -*- coding: utf-8 -*-


from alphaware.utils import (get_tiaocang_date,
                             ensure_noncumul_return,
                             ensure_cumul_return)
from alphaware.enums import FreqType
from alphaware.const import RETURN

print get_tiaocang_date(start_date='2016-01-01', end_date='2016-3-31', freq=FreqType.EOM)

# [datetime.datetime(2016, 1, 29, 0, 0), datetime.datetime(2016, 2, 29, 0, 0), datetime.datetime(2016, 3, 31, 0, 0)]

print get_tiaocang_date(start_date='2017/1/1', end_date='2017/2/1', freq=FreqType.EOW, date_format='%Y/%m/%d')

# [datetime.datetime(2017, 1, 6, 0, 0), datetime.datetime(2017, 1, 13, 0, 0), datetime.datetime(2017, 1, 20, 0, 0),
#  datetime.datetime(2017, 1, 26, 0, 0)]


import pandas as pd
from argcheck import preprocess
from alphaware.utils import (ensure_noncumul_return,
                             ensure_cumul_return)
from alphaware.const import RETURN
from alphaware.enums import ReturnType

# 定义一个累积收益率序列
ret = RETURN(data=pd.Series([1.0, 1.0, 1.05, 1.1],
                            index=['2010-01-02', '2010-01-03', '2010-01-04', '2010-01-05']), type=ReturnType.Cumul)


# 假如用使用日频收益序列，只要结合argcheck.preprocess和ensure_noncumul_return即可
@preprocess(data=ensure_noncumul_return)
def mean_return(data):
    return data.mean()

print mean_return(ret)




