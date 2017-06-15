# -*- coding: utf-8 -*-

from enum import (IntEnum, unique, Enum)


class StrEnum(str, Enum):
    pass


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


@unique
class FactorNormType(IntEnum):
    Null = 0
    Industry_Neutral = 1
    Industry_Cap_Neutral = 2


@unique
class OutputDataFormat(IntEnum):
    MULTI_INDEX_DF = 0
    PITVOT_TABLE_DF = 1
