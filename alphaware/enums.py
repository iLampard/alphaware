# -*- coding: utf-8 -*-

from enum import (IntEnum,
                  unique,
                  Enum)


class StrEnum(str, Enum):
    pass


@unique
class NAStrategy(StrEnum):
    MEAN = 'mean'
    MEDIAN = 'median'
    MOST_FREQ = 'most_frequent'
    CUSTOM = 'custom'


@unique
class FreqType(StrEnum):
    EOD = 'D'
    EOW = 'W'
    EOM = 'M'
    EOQ = 'Q'
    EOSY = 'S'
    EOY = 'Y'


@unique
class FactorType(StrEnum):
    INDUSTY_CODE = 'industry_code'
    ALPHA_FACTOR = 'alpha_factor'
    RETURN = 'return'
    PRICE = 'price'
    ALPHA_FACTOR_MV = 'alpha_factor_mv'
    SCORE = 'score'
    FWD_RETURN = 'fwd_return'


@unique
class FactorNormType(IntEnum):
    Null = 0
    Industry_Neutral = 1
    Industry_Cap_Neutral = 2


@unique
class OutputDataFormat(IntEnum):
    MULTI_INDEX_DF = 0
    PITVOT_TABLE_DF = 1


@unique
class SelectionMethod(StrEnum):
    BRUTAL = 'brutal'
    INDUSTRY_NEUTRAL = 'industry_neutral'


@unique
class ReturnType(IntEnum):
    Non_Cumul = 0
    Cumul = 1
