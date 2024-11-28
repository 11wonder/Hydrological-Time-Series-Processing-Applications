import pandas as pd
from sklearn.impute import KNNImputer
import numpy as np


# 前向填补
def fill_forward(input_filepath, output_filepath, logger=None):
    import pandas as pd

    df = pd.read_excel(input_filepath)

    # 确保 'Date' 列是日期类型
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # 检查是否有有效数据
    if df['Date'].isnull().all():
        message = "No valid date data found!"
        if logger:
            logger(message)
        else:
            print(message)
        return

    # 生成完整的日期范围并填补缺失日期
    start_date = df['Date'].min()
    end_date = df['Date'].max()
    full_range = pd.date_range(start=start_date, end=end_date)
    df_full = pd.DataFrame(index=full_range)
    df_full = df_full.join(df.set_index('Date'), how='left')

    # 前向填补
    df_filled = df_full.ffill(axis=0)  # 按列进行前向填补
    before_filling = f"Before filling: {df_full.isnull().sum()}"
    after_filling = f"After filling: {df_filled.isnull().sum()}"

    if logger:
        logger(before_filling)
        logger(after_filling)
    else:
        print(before_filling)
        print(after_filling)

    # 保存结果
    df_filled.to_excel(output_filepath, index=True)
    success_message = f"Forward fill applied. Output saved to {output_filepath}"
    if logger:
        logger(success_message)
    else:
        print(success_message)


# 后向填补
def fill_backward(input_filepath, output_filepath, logger=None):
    df = pd.read_excel(input_filepath)

    # 确保 'Date' 列是日期类型
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # 检查是否有有效数据
    if df['Date'].isnull().all():
        message = "No valid date data found!"
        if logger:
            logger(message)
        else:
            print(message)
        return

    # 生成完整的日期范围并填补缺失日期
    start_date = df['Date'].min()
    end_date = df['Date'].max()
    full_range = pd.date_range(start=start_date, end=end_date)
    df_full = pd.DataFrame(index=full_range)
    df_full = df_full.join(df.set_index('Date'), how='left')

    # 后向填补
    df_filled = df_full.bfill(axis=0)  # 按列进行后向填补
    before_filling = f"Before filling: {df_full.isnull().sum()}"
    after_filling = f"After filling: {df_filled.isnull().sum()}"

    if logger:
        logger(before_filling)
        logger(after_filling)
    else:
        print(before_filling)
        print(after_filling)

    # 保存结果
    df_filled.to_excel(output_filepath, index=False)  # 保存时不重新写入索引
    success_message = f"Backward fill applied. Output saved to {output_filepath}"
    if logger:
        logger(success_message)
    else:
        print(success_message)




# 线性插值
def fill_linear(input_filepath, output_filepath, logger=None):
    df = pd.read_excel(input_filepath)

    # 确保 'Date' 列是日期类型
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # 检查是否有有效数据
    if df['Date'].isnull().all():
        message = "No valid date data found!"
        if logger:
            logger(message)
        else:
            print(message)
        return

    # 生成完整的日期范围并填补缺失日期
    start_date = df['Date'].min()
    end_date = df['Date'].max()
    full_range = pd.date_range(start=start_date, end=end_date)
    df_full = pd.DataFrame(index=full_range)
    df_full = df_full.join(df.set_index('Date'), how='left')

    # 线性插值
    df_filled = df_full.interpolate(method='linear', axis=0)  # 进行线性插值
    before_filling = f"Before filling: {df_full.isnull().sum()}"
    after_filling = f"After filling: {df_filled.isnull().sum()}"

    if logger:
        logger(before_filling)
        logger(after_filling)
    else:
        print(before_filling)
        print(after_filling)

    # 保存结果
    df_filled.to_excel(output_filepath, index=True)
    success_message = f"Linear interpolation applied. Output saved to {output_filepath}"
    if logger:
        logger(success_message)
    else:
        print(success_message)

# KNN插值
def knn_mean(time_series, window_size):
    result = time_series.copy()
    half_window = window_size // 2
    for idx in range(len(time_series)):
        if np.isnan(time_series[idx]):
            start_idx = max(0, idx - half_window)
            end_idx = min(len(time_series), idx + half_window + 1)
            nearby_values = np.concatenate([time_series[start_idx:idx], time_series[idx + 1:end_idx]])
            result[idx] = np.nanmean(nearby_values)
    return result

def iterative_knn_mean(ts, n, max_iter=100):
    iteration = 0
    while np.isnan(ts).any() and iteration < max_iter:
        ts = knn_mean(ts, n)
        iteration += 1
        print(f"Iteration {iteration}: {np.isnan(ts).sum()} missing values remaining")
    return ts

def fill_knn(input_filepath, output_filepath, n=150, max_iter=100, logger=None):
    df = pd.read_excel(input_filepath)

    # 确保 'Date' 列是日期类型
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # 检查是否有有效数据
    if df['Date'].isnull().all():
        message = "No valid date data found!"
        if logger:
            logger(message)
        else:
            print(message)
        return

    # 生成完整的日期范围并填补缺失日期
    start_date = df['Date'].min()
    end_date = df['Date'].max()
    full_range = pd.date_range(start=start_date, end=end_date)
    df_full = pd.DataFrame(index=full_range)
    df_full = df_full.join(df.set_index('Date'), how='left')

    # 输出填充前的缺失值情况
    before_filling = f"Before filling: {df_full.isnull().sum()}"
    if logger:
        logger(before_filling)
    else:
        print(before_filling)

    # 使用 iterative_knn_mean 进行补全
    df_full['Vertical Displacement (m)'] = iterative_knn_mean(df_full['Vertical Displacement (m)'].values, n, max_iter)

    # 输出填充后的缺失值情况
    after_filling = f"After filling: {df_full.isnull().sum()}"
    if logger:
        logger(after_filling)
    else:
        print(after_filling)

    # 保存结果
    df_full.to_excel(output_filepath, index=True)
    success_message = f"Data saved to {output_filepath}"
    if logger:
        logger(success_message)
    else:
        print(success_message)


# 季节性填补（假设数据中包含季节性趋势，进行基于周期的填补）
def fill_seasonal(input_filepath, output_filepath, logger=None):
    df = pd.read_excel(input_filepath)

    # 确保 'Date' 列是日期类型
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # 检查是否有有效数据
    if df['Date'].isnull().all():
        message = "No valid date data found!"
        if logger:
            logger(message)
        else:
            print(message)
        return

    # 设置 'Date' 为索引
    df.set_index('Date', inplace=True)

    # 生成完整的日期范围并填补缺失日期
    start_date = df.index.min()
    end_date = df.index.max()
    full_range = pd.date_range(start=start_date, end=end_date)
    df_full = pd.DataFrame(index=full_range)
    df_full = df_full.join(df, how='left')

    # 输出填充前的缺失值情况
    before_filling = f"Before filling: {df_full.isnull().sum()}"
    if logger:
        logger(before_filling)
    else:
        print(before_filling)

    # 假设数据按月排序，按周期（12个月）进行季节性填补
    for column in df_full.columns:
        if df_full[column].isnull().any():
            seasonal_filled = df_full[column].interpolate(method='polynomial', order=3)
            df_full[column] = seasonal_filled

    # 输出填充后的缺失值情况
    after_filling = f"After filling: {df_full.isnull().sum()}"
    if logger:
        logger(after_filling)
    else:
        print(after_filling)

    # 保存结果
    df_full.to_excel(output_filepath, index=True)
    success_message = f"Seasonal filling applied. Output saved to {output_filepath}"
    if logger:
        logger(success_message)
    else:
        print(success_message)