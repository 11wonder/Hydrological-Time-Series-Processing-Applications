import os
from Original_Data_Plotting import plot_vertical_displacement
from detrend_processing import detrend_data
from detrend_plotting import plot_detrended_data
from threshold_removal import remove_outliers
from threshold_plotting import plot_threshold_comparison
from detrend_3x_plotting import plot_detrended_3x_data
from Explore_completion_methods import process_data, min_mse_results
from data_completion_methods import fill_forward, fill_backward, fill_linear, fill_knn, fill_seasonal
from final_plotting import plot_filled_data

# 定义文件夹路径
plot_filepath = 'Original_Data_Plotting'
detrend_filepath = 'detrend_data'
threshold_filepath = 'threshold_data'
plot_filepath_detrend = 'detrend_plotting'
plot_filepath_threshold = 'threshold_plotting'
plot_all = 'detrend_removeoutliers_plotting'
final_data_path = 'Final data filling'
final_plot_path = 'Complete and compare the plotting'

# 确保所有输出文件夹存在
os.makedirs(plot_filepath, exist_ok=True)
os.makedirs(detrend_filepath, exist_ok=True)
os.makedirs(threshold_filepath, exist_ok=True)
os.makedirs(plot_filepath_detrend, exist_ok=True)
os.makedirs(plot_filepath_threshold, exist_ok=True)

# 定义 ID 列表
ID_list = [
    "BJFS", "BJGB", "BJSH", "BJYQ", "CHUN", "HECC"
]

def find_input_file(station_id, folders):
    for folder in folders:
        filepath = os.path.join(folder, f"{station_id}.xlsx")
        if os.path.exists(filepath):
            return filepath
    return None

# 文件夹优先级
folders_priority = ["threshold_data", "detrend_data", "Original_Data"]

def main():
    user_input_plot = input("Do you want to plot original images? (yes/no): ").strip().lower()
    if user_input_plot == "yes":
        for station_id in ID_list:
            input_filepath = f'Original_Data/{station_id}.xlsx'
            output_filepath = os.path.join(plot_filepath, f"{station_id}-Original Data.png")
            plot_vertical_displacement(input_filepath, output_filepath)
        print("Original data plots generated successfully.")
    else:
        print("Original data plotting operation cancelled.")

    print("\nChoose the next operation:")
    print("1: No processing")
    print("2: Only detrend the data")
    print("3: Only remove outliers (3x standard deviation)")
    print("4: Detrend and remove outliers")
    user_choice = input("Enter your choice (1/2/3/4): ").strip()

    if user_choice == "1":
        print("No further processing selected. Program completed.")
        user_input_plot = input("Whether to explore methods for data completion (yes/no): ").strip().lower()
        if user_input_plot == "yes":
            print(
                "Description: We will select the longest continuous sequence for blanking and then completion to obtain the best method.")
            hollows = int(input("Please enter an appropriate number of blanks:"))
            for station_id in ID_list:
                input_filepath = f'Original_Data/{station_id}.xlsx'
                process_data(station_id, hollows, input_filepath)
            for ID, (min_mse, methods) in min_mse_results.items():
                print(f"ID: {ID}, Min MSE: {min_mse}, Methods: {', '.join(methods)}")
        else:
            print("Program ended")

    elif user_choice == "2":
        # 去趋势处理
        for station_id in ID_list:
            input_filepath = f'Original_Data/{station_id}.xlsx'
            output_filepath = os.path.join(detrend_filepath, f"{station_id}.xlsx")
            detrend_data(input_filepath, output_filepath)
        print("Detrending completed.")

        # 绘制去趋势图像
        user_input = input("Do you want to plot detrended data? (yes/no): ").strip().lower()
        if user_input == "yes":
            for station_id in ID_list:
                before_filepath = f'Original_Data/{station_id}.xlsx'
                after_filepath = f'detrend_data/{station_id}.xlsx'
                output_filepath = os.path.join(plot_filepath_detrend, f"{station_id}-Detrended.png")
                plot_detrended_data(before_filepath, after_filepath, output_filepath, station_id)
            print("Detrended data plots generated successfully.")
        else:
            print("Detrended data plotting cancelled.")
        user_input_plot = input("Whether to explore methods for data completion (yes/no): ").strip().lower()
        if user_input_plot == "yes":
            print(
                "Description: We will select the longest continuous sequence for blanking and then completion to obtain the best method.")
            hollows = int(input("Please enter an appropriate number of blanks:"))
            for station_id in ID_list:
                input_filepath = f'detrend_data/{station_id}.xlsx'
                process_data(station_id, hollows, input_filepath)
            for ID, (min_mse, methods) in min_mse_results.items():
                print(f"ID: {ID}, Min MSE: {min_mse}, Methods: {', '.join(methods)}")
        else:
            print("Program ended")


    elif user_choice == "3":
        for station_id in ID_list:
            input_filepath = f'Original_Data/{station_id}.xlsx'
            output_filepath = os.path.join(threshold_filepath, f"{station_id}.xlsx")  # 使用全局变量 threshold_filepath
            remove_outliers(input_filepath, output_filepath)
        print("Outlier removal completed.")
        user_input = input("Do you want to plot threshold comparison data? (yes/no): ").strip().lower()
        if user_input == "yes":
            for station_id in ID_list:
                Original_filepath = f'Original_Data/{station_id}.xlsx'
                threshold_file = f'threshold_data/{station_id}.xlsx'  # 修改局部变量名
                output_filepath = os.path.join(plot_filepath_threshold, f"{station_id}-Threshold.png")
                plot_threshold_comparison(Original_filepath, threshold_file, output_filepath, station_id)
            print("Threshold comparison plots generated successfully.")
        else:
            print("Threshold comparison plotting cancelled.")
        user_input_plot = input("Whether to explore methods for data completion (yes/no): ").strip().lower()
        if user_input_plot == "yes":
            print(
                "Description: We will select the longest continuous sequence for blanking and then completion to obtain the best method.")
            hollows = int(input("Please enter an appropriate number of blanks:"))
            for station_id in ID_list:
                input_filepath = f'threshold_data/{station_id}.xlsx'
                process_data(station_id, hollows, input_filepath)
            for ID, (min_mse, methods) in min_mse_results.items():
                print(f"ID: {ID}, Min MSE: {min_mse}, Methods: {', '.join(methods)}")
        else:
            print("Program ended")


    elif user_choice == "4":
        for station_id in ID_list:
            detrend_input_filepath = f'Original_Data/{station_id}.xlsx'
            detrend_output_filepath = os.path.join(detrend_filepath, f"{station_id}.xlsx")
            threshold_output_filepath = os.path.join(threshold_filepath, f"{station_id}.xlsx")
            detrend_data(detrend_input_filepath, detrend_output_filepath)
            remove_outliers(detrend_output_filepath, threshold_output_filepath)
            print(f"Detrending and outlier removal completed for {station_id}.")
        user_input = input("Do you want to plot detrend and threshold comparison data? (yes/no): ").strip().lower()
        if user_input == "yes":
            for station_id in ID_list:
                origin_filepath = f'Original_Data/{station_id}.xlsx'
                detrend_plot_filepath = os.path.join(detrend_filepath, f"{station_id}.xlsx")
                threshold_plot_filepath = os.path.join(threshold_filepath, f"{station_id}.xlsx")
                output_filepath = os.path.join(plot_all, f"{station_id}-Comparison.png")
                plot_detrended_3x_data(origin_filepath, detrend_plot_filepath, threshold_plot_filepath, output_filepath,
                                       station_id)
            print("Detrended and threshold comparison plots generated successfully.")
        else:
            print("Detrended and threshold comparison plotting cancelled.")
        user_input_plot = input("Whether to explore methods for data completion (yes/no): ").strip().lower()
        if user_input_plot == "yes":
            print(
                "Description: We will select the longest continuous sequence for blanking and then completion to obtain the best method.")
            hollows = int(input("Please enter an appropriate number of blanks:"))
            for station_id in ID_list:
                input_filepath = f'threshold_data/{station_id}.xlsx'
                process_data(station_id, hollows, input_filepath)
            for ID, (min_mse, methods) in min_mse_results.items():
                print(f"ID: {ID}, Min MSE: {min_mse}, Methods: {', '.join(methods)}")
        else:
            print("Program ended")

    # 填补方法选择
    user_input_fill = input(
        "Do you want to apply a filling method to complete the missing data? (yes/no): ").strip().lower()
    if user_input_fill == "yes":
        print("Choose a filling method:")
        print("1: Forward Fill")
        print("2: Backward Fill")
        print("3: Linear Interpolation")
        print("4: KNN Imputation")
        print("5: Seasonal Filling")
        user_method = input("Enter your choice (1/2/3/4/5): ").strip()

        fill_method_dict = {
            "1": fill_forward,
            "2": fill_backward,
            "3": fill_linear,
            "4": fill_knn,
            "5": fill_seasonal
        }

        if user_method in fill_method_dict:
            chosen_fill_method = fill_method_dict[user_method]
            print(f"Applying {chosen_fill_method.__name__} method.")
            for station_id in ID_list:
                input_filepath = find_input_file(station_id, folders_priority)
                output_filepath = os.path.join(final_data_path, f"{station_id}-FilledData.xlsx")
                chosen_fill_method(input_filepath, output_filepath)
                plot_output_filepath = os.path.join(final_plot_path, f"{station_id}-FilledComparison.png")
                plot_filled_data(input_filepath, output_filepath, plot_output_filepath, station_id)
            print("Data filling completed with selected method.")
        else:
            print("Invalid choice for filling method.")

    else:
        print("Program ended.")


# 运行主程序
if __name__ == "__main__":
    main()