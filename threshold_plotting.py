import pandas as pd
import os
import matplotlib.pyplot as plt

def plot_threshold_comparison(input_detrend_path, input_threshold_path, output_path, station_id):
    """
    绘制对比图，展示去趋势数据与去除三倍标准差数据的差异。

    Args:
        input_detrend_path (str): 去趋势数据的输入文件路径。
        input_threshold_path (str): 去除三倍标准差数据的输入文件路径。
        output_path (str): 绘图保存路径。
        station_id (str): 站点 ID，用于打印确认信息。
    """
    # 读取数据
    df1 = pd.read_excel(input_detrend_path)
    df2 = pd.read_excel(input_threshold_path)

    # 转换日期列为 datetime 格式
    df1['Date'] = pd.to_datetime(df1['Date'])
    df2['Date'] = pd.to_datetime(df2['Date'])

    # 创建图形
    plt.figure(figsize=(10, 6))

    # 上图：去趋势前的原始数据
    plt.subplot(2, 1, 1)
    plt.plot(df1['Date'], df1['Vertical Displacement (m)'], label='Before Remove outliers')
    plt.title(f'{station_id} - Detrended')  # Title in English
    plt.xlabel('Date')  # X-axis label in English
    plt.ylabel('Vertical Displacement (m)')  # Y-axis label in English
    plt.grid(True)

    # 下图：去趋势后的数据
    plt.subplot(2, 1, 2)
    plt.plot(df2['Date'], df2['Vertical Displacement (m)'], label='After Remove outliers', color='r')
    plt.title(f'{station_id} - Remove 3 Average')  # Title in English
    plt.xlabel('Date')  # X-axis label in English
    plt.ylabel('Vertical Displacement (m)')  # Y-axis label in English
    plt.grid(True)

    # 调整布局并保存图形
    plt.tight_layout()
    plt.savefig(output_path)

    # 关闭图形以释放内存
    plt.close()

    print(f"{station_id}: Comparison plot saved to {output_path}")