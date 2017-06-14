# -*- coding: utf-8 -*-

from datetime import datetime
import pandas as pd
import numpy as np
from PyFin.DateUtilities import (Calendar,
                                 Date,
                                 Period,
                                 Schedule)
from PyFin.Enums import (BizDayConventions,
                         Weekdays)
from argcheck import (expect_types,
                      optional)
from .input_validation import (ensure_pd_series,
                               ensure_pyfin_date)
from .enum import FreqType


@expect_types(date_series=(list, pd.Series, np.ndarray))
def map_to_biz_day(date_series, calendar='China.SSE', convention=BizDayConventions.Preceding):
    """
    :param date_series: array-like of datetime.datetime
    :param calendar: str, optional, 日历名称，见PyFin.DateUtilities.Calendar, default='China.SSE'
    :param convention: str, optional, 如果日期为节假日，如何调整成交易日，见PyFin.DateUtilities.Schedule, default = preceding
    :return: pd.Series, datetime.datetime， 交易日列表
    """
    date_series = ensure_pd_series(date_series)
    unique_date_list = sorted(set(date_series))
    py_date_list = [Date.fromDateTime(date) for date in unique_date_list]
    py_date_list = [Calendar(calendar).adjustDate(date, convention) for date in py_date_list]
    biz_day_list = [Date.toDateTime(date) for date in py_date_list]
    dict_date_map = dict(zip(unique_date_list, biz_day_list))
    ret = date_series.map(dict_date_map)
    return ret


