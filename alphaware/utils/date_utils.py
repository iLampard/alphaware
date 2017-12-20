# -*- coding: utf-8 -*-

from datetime import datetime
from xutils.date_utils import (Calendar,
                               Date,
                               Period,
                               Schedule)
from xutils.date_utils import (BizDayConventions,
                               Weekdays)
from argcheck import (expect_types,
                      preprocess)

from alphaware.enums import FreqType
from .input_validation import (ensure_pd_series,
                               ensure_pyfin_date)


@preprocess(date_series=ensure_pd_series)
def map_to_biz_day(date_series, calendar='China.SSE', convention=BizDayConventions.Preceding):
    """
    :param date_series: array-like of datetime.datetime
    :param calendar: str, optional, 日历名称，见PyFin.DateUtilities.Calendar, default='China.SSE'
    :param convention: str, optional, 如果日期为节假日，如何调整成交易日，见PyFin.DateUtilities.Schedule, default = preceding
    :return: pd.Series, datetime.datetime， 交易日列表
    """
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
    tiaocang_date = Schedule(start_date,
                             end_date,
                             Period('1' + freq),
                             cal,
                             BizDayConventions.Unadjusted)

    if freq.upper() == FreqType.EOW:
        tiaocang_date = [Date.nextWeekday(date, Weekdays.Friday) for date in tiaocang_date]
    elif freq.upper() == FreqType.EOM:
        tiaocang_date = [cal.endOfMonth(date) for date in tiaocang_date]
    elif freq.upper() == FreqType.EOY:
        tiaocang_date = [Date(date.year(), 12, 31) for date in tiaocang_date]

    tiaocang_date = [cal.adjustDate(date, BizDayConventions.Preceding).toDateTime() for date in tiaocang_date if
                     start_date <= date <= end_date]

    return sorted(set(tiaocang_date))
