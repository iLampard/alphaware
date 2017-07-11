# -*- coding: utf-8 -*-

from matplotlib import font_manager
from .date_utils import (map_to_biz_day,
                         get_tiaocang_date)
from .input_validation import (ensure_pd_series,
                               ensure_pd_df,
                               ensure_pyfin_date,
                               ensure_datetime,
                               ensure_np_array,
                               ensure_pd_index_names,
                               ensure_cumul_return,
                               ensure_noncumul_return)
from .pandas_utils import (convert_df_format,
                           top,
                           group_by_freq,
                           quantile_calc)
from .numpy_utils import (index_n_largest,
                          index_n_smallest)

__all__ = ['map_to_biz_day',
           'get_tiaocang_date',
           'ensure_pd_series',
           'ensure_pd_df',
           'ensure_pyfin_date',
           'ensure_datetime',
           'ensure_np_array',
           'ensure_pd_index_names',
           'ensure_cumul_return',
           'ensure_noncumul_return',
           'convert_df_format',
           'index_n_largest',
           'index_n_smallest',
           'top',
           'group_by_freq',
           'fig_style',
           'quantile_calc']


def fig_style(ax, legend, x_label, y_label, legend_loc='upper right'):
    font = font_manager.FontProperties(family='SimHei', style='normal', size=16, weight='normal', stretch='normal')
    ax.legend(legend, prop={'size': 12}, loc=legend_loc)
    ax.title.set_font_properties(font)
    if x_label:
        ax.set_xlabel(x_label)
    if y_label:
        ax.set_ylabel(y_label)
    ax.set_facecolor('white')
    ax.grid(color='gray', alpha=0.2, axis='y')
    return ax
