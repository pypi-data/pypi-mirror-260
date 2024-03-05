import pandas as pd
import numpy as np
from csaps import csaps
from enum import Enum
from typing import List, Optional, Literal


class ValidStats(Enum):
    median = "median"
    var = "var"
    mean = "mean"
    std = "std"
    count = "count"
    sum = "sum"


class NoiseSmoothing(Enum):
    median = "median"
    mean = "mean"
    spline = "spline"


def rolling_stats(df_j,
                  data_names=['Probe1_mV',
                              'Probe6_mV',
                              'Probe4_mV',
                              'Probe5_mV',
                              'Probe3_mV',
                              'Probe2_mV',
                              'Probe1_DegC',
                              'SR2_mV',
                              'SR1_mV'],
                  stat_list: Optional[List[ValidStats]] = ['median', 'var', 'mean', 'count'],
                  time_sampling_s=1800,
                  time_diff=True,
                  sample_period=None
                  ):
    stat_dict = {}

    for data_col in data_names:
        if data_col in df_j.columns:
            stat_dict[data_col] = stat_list
    df_dict = {}
    if sample_period is None:
        time_sampling_si_list = [0, int(time_sampling_s / 2)]
    else:
        time_sampling_si_list = list(range(0, time_sampling_s, sample_period))

    df_rolling = pd.DataFrame()
    df_j['Timestamp'] = pd.to_datetime(df_j['Timestamp'], errors='coerce')
    for time_sampling_si in time_sampling_si_list:
        df = df_j.copy()

        df['Timestamp'] = df['Timestamp'] + pd.Timedelta(seconds=time_sampling_si)

        df['Timestamp_Intv'] = df['Timestamp'].dt.round('{0}S'.format(time_sampling_s))
        df['Timestamp_Intv'] = df['Timestamp_Intv'] - pd.Timedelta(seconds=time_sampling_si)
        df_rolling_i = df.groupby(['Timestamp_Intv', 'ExperimentName']).agg(stat_dict).reset_index()
        df_rolling = pd.concat([df_rolling, df_rolling_i], ignore_index=True)
    df_rolling.columns = ['_'.join(x) if '' != x[-1] else x[0] for x in df_rolling.columns]

    df_rolling.sort_values(by=['Timestamp_Intv'], ascending=True, inplace=True)
    if time_diff:
        df_rolling['Timediff'] = df_rolling['Timestamp_Intv'].shift(-1).subtract(df_rolling['Timestamp_Intv'])
        diff_in = [f'{x}_mean' for x in data_names]
        diff_out = [f'{x}_diff' for x in data_names]
        df_rolling['Timedelta'] = df_rolling['Timestamp_Intv'].shift(-1).subtract(df_rolling['Timestamp_Intv'])
        diff_in = [f'{x}_mean' for x in data_names]
        diff_out = [f'{x}_diff' for x in data_names]
        df_rolling[diff_out] = df_rolling[diff_in].shift(-1).subtract(df_rolling[diff_in])
        df_rolling['Timedelta'] = df_rolling['Timedelta'].dt.total_seconds() / 60
        for diff_i in diff_out:
            df_rolling[diff_i] = df_rolling[diff_i] / df_rolling['Timedelta']
    df_rolling.rename(columns={'Timestamp_Intv': 'Timestamp'}, inplace=True)

    return df_rolling


def calc_spline(df, x_col='Timestamp', y_col='Probe1_mV', smoothing=0.000000000001, tz=None):
    try:
        if not np.issubdtype(df[x_col].dtype, np.number):
            min_time = df[x_col].min()
            df['_Time'] = (df[x_col] - pd.Timestamp(min_time, tz=tz)) / pd.Timedelta('1s')
            return csaps(df['_Time'], df[y_col], df['_Time'], smooth=smoothing)
        else:
            return csaps(df[x_col], df[y_col], df[x_col], smooth=smoothing)
    except:
        min_time = df[x_col].min()
        df['_Time'] = (df[x_col] - pd.Timestamp(min_time, tz=tz)) / pd.Timedelta('1s')
        return csaps(df['_Time'], df[y_col], df['_Time'], smooth=smoothing)
    raise f"{x_col} not a numeric or timestamp"


def calc_noise(df,
               x_col='Timestamp',
               y_col='Probe1_mV',
               smooth_type: Optional[NoiseSmoothing] = 'spline',
               smoothing=0.000000000001,
               tz=None):
    if smooth_type == 'spline':
        df[y_col] = df[y_col].astype(float)
        spline_array = calc_spline(df,
                                   x_col=x_col,
                                   y_col=y_col,
                                   smoothing=smoothing,
                                   tz=tz)
        return df[y_col] - spline_array
    else:
        print('future')
        raise f"This is a futured option"


def calc_rolling_std(df, x_col='Timestamp',
                     y_col='Probe1_mV',
                     time_sampling_s=1800,
                     sampling_period=900,
                     std_type: Optional[Literal['std', 'var']] = 'std',
                     smooth_type: Optional[NoiseSmoothing] = 'spline',
                     smoothing=0.000000000001,
                     tz=None,
                     noise_array=None,
                     append_df=True):
    from datetime import datetime
    if noise_array is None:
        noise_array = calc_noise(df,
                                 x_col=x_col,
                                 y_col=y_col,
                                 smooth_type=smooth_type,
                                 smoothing=smoothing,
                                 tz=tz)
    df[f'{y_col}_noise'] = noise_array
    df2 = rolling_stats(df,
                        data_names=[f'{y_col}_noise'],
                        stat_list=[std_type],
                        time_sampling_s=time_sampling_s,
                        time_diff=False,
                        sample_period=sampling_period
                        )
    if append_df:
        drop_list = set(df2.columns).intersection(set(df.columns)) - set([x_col])

        df2.drop(columns=drop_list, inplace=True)
        df2 = pd.merge_asof(left=df, right=df2, left_on=x_col, right_on=x_col, direction='nearest',
                            tolerance=pd.Timedelta(f'{sampling_period} s'))
        df2[f'{y_col}_noise_{std_type}'] = df2[f'{y_col}_noise_{std_type}'].interpolate(method='linear')
    return df2


def find_daily_min(df, x_col='Timestamp',
                   y_col='Probe1_mV',
                   start_time='00:00',
                   end_time='12:30',
                   smooth_type: Optional[NoiseSmoothing] = 'spline',
                   smoothing=0.000000000001,
                   sampling_period=None,
                   tz=None):
    from datetime import datetime
    spline_col = f'{y_col}_spline'
    df[spline_col] = calc_spline(df, x_col=x_col, y_col=y_col, smoothing=smoothing, tz=tz)
    df.index = df[x_col]
    df.index.name = f'index'
    df_2 = df.between_time(start_time, end_time)
    datetime_str = f'2016-01-02 {start_time}:00 +00:00'
    start_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S %z')
    df_2['Day_Group'] = (df_2.index - start_datetime).days
    df_2 = df_2.groupby('Day_Group').apply(
        lambda x: x[(x[spline_col] == x[spline_col].min())].agg({'Timestamp': 'mean', spline_col: 'mean'}))
    drop_list = list(set(df_2.columns).intersection(set(df.columns)) - {x_col, spline_col})
    df_2.drop(columns=drop_list, inplace=True)
    time1 = datetime.strptime(end_time, "%H:%M")  # convert string to time
    time2 = datetime.strptime(start_time, "%H:%M")
    diff = time1 - time2
    diff = diff.total_seconds()

    if sampling_period is None:
        sampling_period = df['Timestamp'].shift(-1).subtract(df['Timestamp']).median()
    sampling_period = sampling_period * 10
    df_2.rename(columns={spline_col: f'{y_col}_day_min'}, inplace=True)
    df_2.index.name = f'index'
    x = pd.merge_asof(left=df_2, right=df.reset_index(), left_on=x_col, right_on=x_col, direction='nearest',
                      tolerance=pd.Timedelta(f'{sampling_period} s'))
    merged_df = df.merge(x[[f'{y_col}_day_min', 'index']], how='left', left_index=True, right_on='index').set_index(
        'index')
    merged_df[f'{y_col}_day_min'] = merged_df.set_index(x_col)[f'{y_col}_day_min'].interpolate('index').values
    merged_df[f'{y_col}_min_sub'] = merged_df[spline_col] - merged_df[f'{y_col}_day_min']
    return merged_df


def find_rolling_sum(df, x_col='Timestamp',
                     y_col='Probe1_mV',
                     start_time='00:00',
                     end_time='12:30',
                     smooth_type: Optional[NoiseSmoothing] = 'spline',
                     smoothing=0.000000000001,
                     sampling_period=1800,
                     time_sampling_s=24 * 60 * 60,
                     tz=None):
    merged_df = find_daily_min(df, x_col=x_col,
                               y_col=y_col,
                               start_time=start_time,
                               end_time=end_time,
                               smooth_type=smooth_type,
                               smoothing=smoothing,
                               sampling_period=sampling_period,
                               tz=None)
    merged_df2 = rolling_stats(merged_df,
                               data_names=[f'{y_col}_min_sub'],
                               stat_list=['sum'],
                               time_sampling_s=time_sampling_s,
                               sample_period=sampling_period,
                               time_diff=False
                               )
    x_col = 'Timestamp'
    sampling_period = 1800
    drop_list = set(merged_df2.columns).intersection(set(merged_df.columns)) - set([x_col])
    merged_df2.drop(columns=drop_list, inplace=True)
    merged_df2 = pd.merge_asof(left=merged_df, right=merged_df2, left_on=x_col, right_on=x_col, direction='nearest',
                               tolerance=pd.Timedelta(f'{sampling_period} s'))
    merged_df2[f'{y_col}_sub_sum'] = merged_df2[f'{y_col}_min_sub_sum'].interpolate(
        method='linear')
    merged_df2[f'Probe1_mV_auc'] = merged_df2[f'{y_col}_min_sub_sum'] / time_sampling_s
    return merged_df2


def rolling_integrate(df, x_col='Timestamp',
                      y_col='Probe1_mV',
                      start_time='00:00',
                      end_time='12:30',
                      smooth_type: Optional[NoiseSmoothing] = 'spline',
                      smoothing=0.000000000001,
                      sampling_period=1800,
                      time_sampling_s=24 * 60 * 60,
                      tz=None):
    df_mp = find_daily_min(df, x_col=x_col,
                           y_col=y_col,
                           start_time=start_time,
                           end_time=end_time,
                           smooth_type=smooth_type,
                           smoothing=smoothing,
                           sampling_period=sampling_period,
                           tz=tz)

    df_mp['Timediff'] = df_mp['Timestamp'].shift(-1).subtract(df_mp['Timestamp']).dt.total_seconds()
    df_mp['int_dx'] = (df_mp['Timediff'] * df_mp[f'{y_col}_min_sub'] + df_mp['Timediff'] * df_mp[
        f'{y_col}_min_sub'].shift(-1)) / 2
    df_mp[f'{y_col}_integral'] = df_mp.rolling(f'{time_sampling_s} s', center=True)['int_dx'].sum() / time_sampling_s
    min_timestamp = min(df_mp['Timestamp']) + pd.Timedelta(seconds=time_sampling_s / 2)
    max_timestamp = max(df_mp['Timestamp']) - pd.Timedelta(seconds=time_sampling_s / 2)
    df_mp.drop(columns=['Timediff', 'int_dx'], inplace=True)
    df_mp.loc[(df_mp['Timestamp'] > max_timestamp) | (df_mp['Timestamp'] < min_timestamp), f'{y_col}_integral'] = np.nan

    return df_mp
