# -*- coding: utf-8 -*-


import pandas as pd
from datetime import datetime
from argcheck import expect_types
from PyFin.DateUtilities import Date


def ensure_pd_series(data):
    if isinstance(data, pd.Series):
        return data
    try:
        return pd.Series(data)
    except Exception as e:
        raise 'Error in ensure_pd_series: {0}'.format(e)


@expect_types(date=(str, unicode, datetime))
def ensure_pyfin_date(date, date_format='%Y-%m-%d'):
    """
    :param date: str, unicode, datetime, 日期
    :param date_format: str, 时间格式
    :return: PyFin.Date object 
    """
    if isinstance(date, str) or isinstance(date, unicode):
        return Date.strptime(date, date_format)
    else:
        return Date.fromDateTime(date)
