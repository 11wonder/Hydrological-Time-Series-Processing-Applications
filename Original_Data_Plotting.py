# plot_functions.py
import pandas as pd
import matplotlib.pyplot as plt
import os


def plot_vertical_displacement(input_filepath, output_filepath):
    """
    读取Excel文件，绘制并保存垂直位移图
    """
    # 读取数据
    df = pd.read_excel(input_filepath)

    # 转换日期列为日期格式
    df['Date'] = pd.to_datetime(df['Date'])

    # 绘制图形
    plt.figure(figsize=(10, 3))
    plt.plot(df['Date'], df['Vertical Displacement (m)'])
    plt.title(f'{os.path.basename(input_filepath)} - Original Data')  # Title using file name
    plt.xlabel('Date')  # X-axis label
    plt.ylabel('Vertical Displacement (m)')  # Y-axis label
    plt.grid(True)

    # 保存图形
    plt.tight_layout()
    plt.savefig(output_filepath)
    plt.close()

    print(f"Original Data plot saved for {os.path.basename(input_filepath)}: {output_filepath}")