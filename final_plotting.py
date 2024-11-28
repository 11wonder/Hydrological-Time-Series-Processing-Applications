import matplotlib.pyplot as plt
import pandas as pd
def plot_filled_data(input_filepath_original, input_filepath_filled, output_filepath, station_id):
    # 读取原始数据和填补后的数据
    df_original = pd.read_excel(input_filepath_original)
    df_filled = pd.read_excel(input_filepath_filled)

    # 确保日期为时间格式并设置为索引
    df_original['Date'] = pd.to_datetime(df_original['Date'], errors='coerce')
    df_filled.iloc[:, 0] = pd.to_datetime(df_filled.iloc[:, 0], errors='coerce')
    df_filled.rename(columns={df_filled.columns[0]: 'Date'}, inplace=True)

    df_original.set_index('Date', inplace=True)
    df_filled.set_index('Date', inplace=True)

    # 确保日期范围对齐
    start_date = df_original.index.min()
    end_date = df_original.index.max()
    full_range = pd.date_range(start=start_date, end=end_date)

    df_original_full = df_original.reindex(full_range)
    df_filled_full = df_filled.reindex(full_range)

    # 创建图形
    plt.figure(figsize=(10, 4))

    # 原始数据
    plt.scatter(df_original_full.index, df_original_full['Vertical Displacement (m)'],
                label='Original Data', color='red', s=1)


    # 标注填补点
    missing_idx = df_original_full['Vertical Displacement (m)'].isna()
    plt.scatter(df_filled_full.index[missing_idx], df_filled_full['Vertical Displacement (m)'][missing_idx],
                label='Filled Points', color='black', s=5)

    # 设置标题和标签
    plt.title(f'{station_id} - Filled Data Comparison')
    plt.xlabel('Date')
    plt.ylabel('Displacement (m)')
    plt.legend()
    plt.grid(True)

    # 保存图像
    plt.tight_layout()
    plt.savefig(output_filepath)
    plt.close()
    print(f"Filled data plot saved for {station_id}: {output_filepath}")