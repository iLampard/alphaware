# -*- coding: utf-8 -*-


from ctypes import (
    Structure,
    c_ubyte,
    c_uint,
    c_ulong,
    c_ulonglong,
    c_ushort,
    sizeof,
)
import numpy as np
import pandas as pd
from six.moves import range

_INTTYPES_MAP = {
    sizeof(t) - 1: t for t in {
    c_ubyte,
    c_uint,
    c_ulong,
    c_ulonglong,
    c_ushort}
}

_INTTYPES = list(
    pd.Series(_INTTYPES_MAP).reindex(
        range(max(_INTTYPES_MAP.keys())),
        method='bfill',
    ),
)


def enum(option, *options):
    """
    https://github.com/quantopian/zipline/blob/e1b27c45ae4b881e5416a5c50e8945232527ea59/zipline/utils/enum.py
    """
    options = (option,) + options
    rangeob = range(len(options))

    try:
        inttype = _INTTYPES[int(np.log2(len(options) - 1)) // 8]
    except IndexError:
        raise OverflowError(
            'Cannot store enums with more than sys.maxsize elements, got %d' %
            len(options),
        )

    class _enum(Structure):
        _fields_ = [(o, inttype) for o in options]

        def __iter__(self):
            return iter(rangeob)

        def __contains__(self, value):
            return 0 <= value < len(options)

        def __repr__(self):
            return '<enum: %s>' % (
                ('%d fields' % len(options))
                if len(options) > 10 else
                repr(options)
            )

    return _enum(*rangeob)


FreqType = enum('EOD', 'EOW', 'EOM', 'EOQ', 'EOSY', 'EOY')
