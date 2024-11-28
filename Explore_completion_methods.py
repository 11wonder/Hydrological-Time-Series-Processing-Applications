import pandas as pd
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np

min_mse_results = {}

def process_data(ID,x,input_filepath):
    df = pd.read_excel(input_filepath)
    df.set_index('Date', inplace=True)
    df.rename(columns={'Date': 'date', 'Vertical Displacement (m)': 'value'}, inplace=True)

    # 备份原始数据
    df_orig = df.copy()
    df_orig.index = pd.to_datetime(df_orig.index)
    df_orig['diff'] = df_orig.index.to_series().diff().dt.days
    df_orig['group'] = (df_orig['diff'] > 1).cumsum()
    longest_group = df_orig.groupby('group').size().idxmax()
    df_orig = df_orig[df_orig['group'] == longest_group]
    df_orig = df_orig.drop(columns=['diff', 'group'])

    # 随机选择缺失值
    random_indices = df_orig.sample(n=x, random_state=42).index  # 删除100个点
    df = df_orig.copy()
    df.loc[random_indices, 'value'] = np.nan

    # 创建子图
    fig, axes = plt.subplots(6, 1, sharex=True, figsize=(10, 6))
    plt.rcParams.update({'xtick.bottom': False})

    # 原始数据绘图
    df_orig.plot(title='Actual', ax=axes[0], label='Actual', color='black', style="-")
    df.plot(title='Actual', ax=axes[0], label='Actual', color='red', style="-")
    axes[0].legend(["Missing Data", "Available Data"])

    mse_results = {}  # 存储每种插值方法的 MSE

    # 插值方法：Forward Fill
    mse_results["Forward Fill"] = fill_forward(df, df_orig, axes[1])

    # 插值方法：Backward Fill
    mse_results["Backward Fill"] = fill_backward(df, df_orig, axes[2])

    # 插值方法：Linear Interpolation
    mse_results["Linear Fill"] = fill_linear(df, df_orig, axes[3])

    # 插值方法：KNN
    mse_results["KNN Mean"] = fill_knn(df, df_orig, axes[4])

    # 插值方法：Seasonal Mean
    mse_results["Seasonal Mean"] = fill_seasonal(df, df_orig, axes[5])

    # 保存图片
    plt.tight_layout()
    plt.savefig(f"Explore completion methods/{ID}_plot.png")
    plt.close()

    # 找到最小 MSE 及其对应方法
    min_mse = min(mse_results.values())
    min_method = [method for method, mse in mse_results.items() if mse == min_mse]
    min_mse_results[ID] = (min_mse, min_method)


# 各种插值方法的实现

def fill_forward(df, df_orig, ax):
    df_ffill = df.ffill()
    common_index = df_orig['value'].notna() & df_ffill['value'].notna()
    error_ffill = np.round(mean_squared_error(df_orig.loc[common_index, 'value'], df_ffill.loc[common_index, 'value']), 10)
    df_ffill['value'].plot(title=f"Forward Fill (MSE: {error_ffill})", ax=ax, label="Forward Fill", style="-")
    return error_ffill


def fill_backward(df, df_orig, ax):
    df_bfill = df.bfill()
    common_index = df_orig['value'].notna() & df_bfill['value'].notna()
    error_bfill = np.round(mean_squared_error(df_orig.loc[common_index, 'value'], df_bfill.loc[common_index, 'value']), 10)
    df_bfill['value'].plot(title=f"Backward Fill (MSE: {error_bfill})", ax=ax, label="Backward Fill", color="firebrick", style="-")
    return error_bfill


def fill_linear(df, df_orig, ax):
    df_linear = df.interpolate(method="linear")
    common_index = df_orig['value'].notna() & df_linear['value'].notna()
    error_linear = np.round(mean_squared_error(df_orig.loc[common_index, 'value'], df_linear.loc[common_index, 'value']), 10)
    df_linear['value'].plot(title=f"Linear Fill (MSE: {error_linear})", ax=ax, label="Linear Fill", color="brown", style="-")
    return error_linear


def fill_knn(df, df_orig, ax):
    df['knn_mean'] = knn_imputation(df['value'].values, window_size=8)
    common_index = df_orig['value'].notna() & df['knn_mean'].notna()
    error_knn = np.round(mean_squared_error(df_orig.loc[common_index, 'value'], df.loc[common_index, 'knn_mean']), 10)
    df['knn_mean'].plot(title=f"KNN (MSE: {error_knn})", ax=ax, label='KNN', color='tomato', alpha=0.5, style='-')
    return error_knn


def knn_imputation(time_series, window_size):
    result = time_series.copy()
    half_window = window_size // 2
    for idx in range(len(time_series)):
        if np.isnan(time_series[idx]):
            start_idx = max(0, idx - half_window)
            end_idx = min(len(time_series), idx + half_window + 1)
            nearby_values = np.concatenate([time_series[start_idx:idx], time_series[idx + 1:end_idx]])
            result[idx] = np.nanmean(nearby_values)
    return result


def fill_seasonal(df, df_orig, ax):
    df['seasonal_mean'] = seasonal_imputation(df['value'], season_length=12, smoothing_factor=1.25)
    common_index = df_orig['value'].notna() & df['seasonal_mean'].notna()
    error_seasonal = np.round(mean_squared_error(df_orig.loc[common_index, 'value'], df.loc[common_index, 'seasonal_mean']), 10)
    df['seasonal_mean'].plot(title=f"Seasonal Mean (MSE: {error_seasonal})", ax=ax, label='Seasonal Mean', color='blue', alpha=0.5, style='-')
    return error_seasonal


def seasonal_imputation(time_series, season_length, smoothing_factor):
    result = np.copy(time_series)
    for idx, value in enumerate(time_series):
        if np.isnan(value):
            seasonal_values = time_series[idx - 1::-season_length]
            if np.isnan(np.nanmean(seasonal_values)):
                seasonal_values = np.concatenate([time_series[idx - 1::-season_length], time_series[idx::season_length]])
            result[idx] = np.nanmean(seasonal_values) * smoothing_factor
    return result
