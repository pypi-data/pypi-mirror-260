try:
    from algaestat.version import version as __version__
except ImportError:
    __version__ = '0.0.1.unknown'

import pandas as pd
import algaestat
from algaestat.io.dynamo import QueryDB, get_tableinfo, get_write_tableinfo
from algaestat.utils.aggregate import (rolling_stats, calc_spline, calc_noise, calc_rolling_std, find_daily_min,
                                       rolling_integrate)
