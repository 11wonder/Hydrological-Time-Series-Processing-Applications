import pandas as pd
from scipy import signal
import os

def detrend_data(input_filepath, output_filepath):
    """
    读取文件，进行去趋势处理，并保存结果。

    Args:
        input_filepath (str): 输入文件路径。
        output_filepath (str): 输出文件路径。
    """
    # 读取 Excel 文件
    df = pd.read_excel(input_filepath)

    # 设置索引
    df.set_index('Date', inplace=True)

    # 提取垂直位移数据
    vertical_displacement = df['Vertical Displacement (m)']

    # 对数据进行去趋势操作
    detrended_values = signal.detrend(vertical_displacement)

    # 将去趋势后的数据添加到 DataFrame 中
    df['Vertical Displacement (m)'] = detrended_values

    # 保存去趋势后的数据到新的 Excel 文件
    df.to_excel(output_filepath)

    print(f"Detrended data saved: {output_filepath}")