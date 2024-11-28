import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_detrended_data(before_filepath, after_filepath, output_filepath, station_id):
    """
    绘制去趋势前后的对比图，并保存到文件。

    Args:
        before_filepath (str): 去趋势前数据文件路径。
        after_filepath (str): 去趋势后数据文件路径。
        output_filepath (str): 输出图像文件路径。
        station_id (str): 站点 ID，用于标题标注。
    """
    # 读取去趋势前后的数据
    df1 = pd.read_excel(before_filepath)
    df2 = pd.read_excel(after_filepath)

    # 确保 Date 列为 datetime 格式
    df1['Date'] = pd.to_datetime(df1['Date'])
    df2['Date'] = pd.to_datetime(df2['Date'])

    # 创建绘图
    plt.figure(figsize=(10, 6))

    # 上图：去趋势前的原始数据
    plt.subplot(2, 1, 1)
    plt.plot(df1['Date'], df1['Vertical Displacement (m)'], label='Before Detrend')
    plt.title(f'{station_id} - Before Detrend')  # Title in English
    plt.xlabel('Date')  # X-axis label in English
    plt.ylabel('Vertical Displacement (m)')  # Y-axis label in English
    plt.grid(True)

    # 下图：去趋势后的数据
    plt.subplot(2, 1, 2)
    plt.plot(df2['Date'], df2['Vertical Displacement (m)'], label='After Detrend', color='r')
    plt.title(f'{station_id} - After Detrend')  # Title in English
    plt.xlabel('Date')  # X-axis label in English
    plt.ylabel('Vertical Displacement (m)')  # Y-axis label in English
    plt.grid(True)

    # 调整布局并保存图片
    plt.tight_layout()
    plt.savefig(output_filepath)
    plt.close()

    print(f"Plot saved for {station_id}: {output_filepath}")