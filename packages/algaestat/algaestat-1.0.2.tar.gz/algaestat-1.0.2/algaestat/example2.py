import pandas as pd
import os
import algaestat
from typing import Optional

df = pd.read_csv('~/miprobe_data.csv')

df['Timestamp'] = pd.to_datetime(df['Timestamp'])
merged_df = algaestat.rolling_integrate(df, x_col='Timestamp',
                                        y_col='MP1',
                                        start_time='00:00',
                                        end_time='12:30',
                                        smooth_type='spline',
                                        smoothing=0.000000000001,
                                        sampling_period=1800,
                                        time_sampling_s=24 * 60 * 60,
                                        tz=None)
print(merged_df)
merged_df.to_csv('~/miprobe_data_auc_out.csv')
