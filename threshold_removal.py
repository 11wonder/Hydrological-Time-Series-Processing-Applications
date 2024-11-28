import pandas as pd
import os

def remove_outliers(input_filepath, output_filepath):
    """
    去除数据中超过三倍标准差的异常值并保存。

    Args:
        input_filepath (str): 输入文件路径。
        output_filepath (str): 输出文件路径。
    """
    # 读取数据
    df = pd.read_excel(input_filepath)

    # 确保 'Date' 列存在并转换为日期时间格式
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    else:
        raise ValueError(f"The input file '{input_filepath}' does not contain a 'Date' column.")

    # 计算均值和标准差
    mean = df['Vertical Displacement (m)'].mean()
    std = df['Vertical Displacement (m)'].std()

    # 定义上下阈值
    upper_threshold = mean + 3 * std
    lower_threshold = mean - 3 * std

    # 去除异常值
    df_cleaned = df[(df['Vertical Displacement (m)'] >= lower_threshold) &
                    (df['Vertical Displacement (m)'] <= upper_threshold)]


    # 确保输出文件夹存在
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)

    # 保存到新文件
    df_cleaned.to_excel(output_filepath, index=False, engine='openpyxl')

    print(f"Outliers removed and adjusted data saved to {output_filepath}")