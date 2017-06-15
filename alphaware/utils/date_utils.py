# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from datetime import datetime
from PyFin.DateUtilities import (Calendar,
                                 Date,
                                 Period,
                                 Schedule)
from PyFin.Enums import (BizDayConventions,
                         Weekdays)
from argcheck import (expect_types,
                      expect_element,
                      optional)
from .input_validation import (ensure_pd_series,
                               ensure_pyfin_date)
from .enums import FreqType


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


@expect_types(start_date=(str, datetime), end_date=(str, datetime), freq=(str, FreqType))
def get_tiaocang_date(start_date, end_date, freq=FreqType.EOM, calendar='China.SSE', date_format='%Y-%m-%d'):
    """
    :param start_date: str/datetime.datetime, 开始日期
    :param end_date: str/datetime.datetime, 结束日期
    :param freq: str enum, default=EOM, 月度
    :param calendar: str, 日历名称
    :param date_format: str, start_date/end_date 如果是str格式，其格式的日期形式
    :return: list, datetime.datetime
    返回在开始日至结束日之间的调仓日(交易日)
    """
    calendar = calendar
    date_format = date_format
    start_date = ensure_pyfin_date(start_date, date_format)
    end_date = ensure_pyfin_date(end_date, date_format)

    cal = Calendar(calendar)

    if freq.upper() == FreqType.EOW:
        start_date = Date.nextWeekday(start_date, Weekdays.Friday)
        end_date = Date.nextWeekday(end_date, Weekdays.Friday)
    elif freq.upper() == FreqType.EOM:
        start_date = cal.endOfMonth(start_date)
        end_date = cal.endOfMonth(end_date)
    elif freq.upper() == FreqType.EOY:
        start_date = Date(start_date.year(), 1, 1)
        end_date = Date(end_date.year(), 12, 31)

    tiaocang_date = Schedule(start_date,
                             end_date,
                             Period('1' + freq),
                             cal,
                             BizDayConventions.Preceding)

    tiaocang_date = [date.toDateTime() for date in tiaocang_date[:-1] if start_date <= date <= end_date]
    return tiaocang_date
