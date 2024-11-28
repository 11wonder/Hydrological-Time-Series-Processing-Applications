import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel,
    QTextBrowser, QRadioButton, QButtonGroup, QGraphicsView, QGraphicsScene,
    QGraphicsPixmapItem, QInputDialog, QMessageBox
)
from PyQt5.QtGui import QPixmap
from Original_Data_Plotting import plot_vertical_displacement
from detrend_processing import detrend_data
from detrend_plotting import plot_detrended_data
from threshold_removal import remove_outliers
from threshold_plotting import plot_threshold_comparison
from detrend_3x_plotting import plot_detrended_3x_data
from Explore_completion_methods import process_data, min_mse_results
from data_completion_methods import fill_forward, fill_backward, fill_linear, fill_knn, fill_seasonal
from final_plotting import plot_filled_data

# 文件夹路径
PLOT_FILEPATH = 'Original_Data_Plotting'
DETREND_FILEPATH = 'detrend_data'
THRESHOLD_FILEPATH = 'threshold_data'
FINAL_DATA_PATH = 'Final data filling'
FINAL_PLOT_PATH = 'Complete and compare the plotting'
plot_filepath_detrend = 'detrend_plotting'
plot_filepath_threshold = 'threshold_plotting'
plot_all = 'detrend_removeoutliers_plotting'
plot_explore = 'Explore completion methods'
folder_path = "Original_Data"

# 确保所有输出文件夹存在
os.makedirs(PLOT_FILEPATH, exist_ok=True)
os.makedirs(DETREND_FILEPATH, exist_ok=True)
os.makedirs(THRESHOLD_FILEPATH, exist_ok=True)
os.makedirs(FINAL_DATA_PATH, exist_ok=True)
os.makedirs(FINAL_PLOT_PATH, exist_ok=True)

# ID 列表
def get_xlsx_file_names(folder_path):
    """
    从指定文件夹中读取所有 .xlsx 文件的名字（不包含扩展名），
    并返回以逗号分隔的列表格式。

    Args:
        folder_path (str): 文件夹路径

    Returns:
        list: 文件名列表（不包含扩展名）
    """
    # 获取文件夹中的所有文件
    files = os.listdir(folder_path)
    # 筛选出 .xlsx 文件并去掉扩展名
    id_list = [os.path.splitext(file)[0] for file in files if file.endswith('.xlsx')]
    return id_list

ID_LIST = get_xlsx_file_names(folder_path)

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hydrological Time Series Processing Applications")  #Hydrological Time Series Processing Applications
        self.setGeometry(200, 200, 1000, 600)
        self.current_image_index = 0
        self.image_list = []
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        # 左侧布局
        left_layout = QVBoxLayout()
        self.title_label = QLabel("Data Processing Tool", self)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        left_layout.addWidget(self.title_label)

        self.instruction_browser = QTextBrowser(self)
        self.instruction_browser.setFixedWidth(300)
        self.instruction_browser.setText("选择操作按钮以开始数据处理。")
        left_layout.addWidget(self.instruction_browser)

        # 添加功能按钮
        self.add_buttons(left_layout)
        layout.addLayout(left_layout)

        # 右侧图片显示
        right_layout = QVBoxLayout()
        self.image_view = QGraphicsView(self)
        self.image_scene = QGraphicsScene()
        self.image_view.setScene(self.image_scene)
        right_layout.addWidget(self.image_view)

        # 图片翻页按钮
        btn_layout = QHBoxLayout()
        self.btn_prev = QPushButton("Previous")
        self.btn_prev.clicked.connect(self.show_previous_image)
        btn_layout.addWidget(self.btn_prev)

        self.btn_next = QPushButton("Next")
        self.btn_next.clicked.connect(self.show_next_image)
        btn_layout.addWidget(self.btn_next)
        right_layout.addLayout(btn_layout)

        layout.addLayout(right_layout)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def log_message(self, message):
        """向文本框中追加日志信息"""
        self.instruction_browser.append(message)

    def add_buttons(self, layout):
        btn_plot_original = QPushButton("Plot Original Data")
        btn_plot_original.clicked.connect(self.plot_original_data)
        layout.addWidget(btn_plot_original)

        self.add_detrend_options(layout)

        btn_explore_methods = QPushButton("Explore Completion Methods")
        btn_explore_methods.clicked.connect(self.explore_methods)
        layout.addWidget(btn_explore_methods)

        btn_fill_data = QPushButton("Fill Missing Data")
        btn_fill_data.clicked.connect(self.fill_missing_data)
        layout.addWidget(btn_fill_data)

    def add_detrend_options(self, layout):
        self.detrend_group = QButtonGroup(self)
        self.detrend_buttons = [
            QRadioButton("1: No processing"),
            QRadioButton("2: Only detrend the data"),
            QRadioButton("3: Only remove outliers (3x standard deviation)"),
            QRadioButton("4: Detrend and remove outliers")
        ]
        for i, button in enumerate(self.detrend_buttons):
            self.detrend_group.addButton(button, i + 1)
            layout.addWidget(button)
        self.detrend_buttons[0].setChecked(True)

        btn_execute = QPushButton("Execute")
        btn_execute.clicked.connect(self.execute_processing)
        layout.addWidget(btn_execute)

    def load_images_from_directory(self, directory):
        self.image_list = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(('.png', '.jpg', '.jpeg'))]
        self.current_image_index = 0
        if self.image_list:
            self.show_image()

    def show_image(self):
        if self.image_list:
            image_path = self.image_list[self.current_image_index]
            pixmap = QPixmap(image_path)
            self.image_scene.clear()
            self.image_scene.addItem(QGraphicsPixmapItem(pixmap))

    def show_previous_image(self):
        if self.image_list:
            self.current_image_index = (self.current_image_index - 1) % len(self.image_list)
            self.show_image()

    def show_next_image(self):
        if self.image_list:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_list)
            self.show_image()

    def plot_original_data(self):
        self.instruction_browser.setText("正在绘制原始数据……")
        for station_id in ID_LIST:
            input_filepath = f'Original_Data/{station_id}.xlsx'
            output_filepath = os.path.join(PLOT_FILEPATH, f"{station_id}-Original Data.png")
            if os.path.exists(input_filepath):
                plot_vertical_displacement(input_filepath, output_filepath)
            else:
                self.instruction_browser.append(f"{input_filepath} 不存在。")
        self.load_images_from_directory(PLOT_FILEPATH)
        self.instruction_browser.append("原始数据绘图完成。")

    def execute_processing(self):
        selected_id = self.detrend_group.checkedId()
        if selected_id == 1:
            self.no_processing()
        elif selected_id == 2:
            self.only_detrend()
        elif selected_id == 3:
            self.only_remove_outliers()
        elif selected_id == 4:
            self.detrend_and_remove_outliers()

    def no_processing(self):
        self.instruction_browser.append("No processing selected. Operation completed.")

    def only_detrend(self):
        self.instruction_browser.setText("正在进行去趋势处理……")
        for station_id in ID_LIST:
            input_filepath = f'Original_Data/{station_id}.xlsx'
            output_filepath = os.path.join(DETREND_FILEPATH, f"{station_id}.xlsx")
            if os.path.exists(input_filepath):
                detrend_data(input_filepath, output_filepath)
            else:
                QMessageBox.warning(self, "File Not Found", f"{input_filepath} 不存在。")
        for station_id in ID_LIST:
            before_filepath = f'Original_Data/{station_id}.xlsx'
            after_filepath = f'detrend_data/{station_id}.xlsx'
            output_filepath_1 = os.path.join(plot_filepath_detrend, f"{station_id}-Detrended.png")
            plot_detrended_data(before_filepath, after_filepath, output_filepath_1, station_id)
        self.load_images_from_directory(plot_filepath_detrend)
        self.instruction_browser.append("去趋势处理完成。")

    def only_remove_outliers(self):
        self.instruction_browser.setText("正在移除异常值……")
        for station_id in ID_LIST:
            input_filepath = f'Original_Data/{station_id}.xlsx'
            output_filepath = os.path.join(THRESHOLD_FILEPATH, f"{station_id}.xlsx")
            if os.path.exists(input_filepath):
                remove_outliers(input_filepath, output_filepath)
            else:
                QMessageBox.warning(self, "File Not Found", f"{input_filepath} 不存在。")
        for station_id in ID_LIST:
            Original_filepath = f'Original_Data/{station_id}.xlsx'
            threshold_file = f'threshold_data/{station_id}.xlsx'  # 修改局部变量名
            output_filepath = os.path.join(plot_filepath_threshold, f"{station_id}-Threshold.png")
            plot_threshold_comparison(Original_filepath, threshold_file, output_filepath, station_id)
        self.load_images_from_directory(plot_filepath_threshold)
        self.instruction_browser.append("异常值移除完成。")

    def detrend_and_remove_outliers(self):
        self.instruction_browser.setText("正在进行去趋势和移除异常值操作……")
        for station_id in ID_LIST:
            input_filepath = f'Original_Data/{station_id}.xlsx'
            detrend_output_filepath = os.path.join(DETREND_FILEPATH, f"{station_id}.xlsx")
            threshold_output_filepath = os.path.join(THRESHOLD_FILEPATH, f"{station_id}.xlsx")
            if os.path.exists(input_filepath):
                detrend_data(input_filepath, detrend_output_filepath)
                remove_outliers(detrend_output_filepath, threshold_output_filepath)
            else:
                QMessageBox.warning(self, "File Not Found", f"{input_filepath} 不存在。")
        for station_id in ID_LIST:
            origin_filepath = f'Original_Data/{station_id}.xlsx'
            detrend_plot_filepath = os.path.join(DETREND_FILEPATH, f"{station_id}.xlsx")
            threshold_plot_filepath = os.path.join(THRESHOLD_FILEPATH, f"{station_id}.xlsx")
            output_filepath = os.path.join(plot_all, f"{station_id}-Comparison.png")
            plot_detrended_3x_data(origin_filepath, detrend_plot_filepath, threshold_plot_filepath, output_filepath,
                                   station_id)
        self.load_images_from_directory(plot_all)
        self.instruction_browser.append("去趋势和异常值移除完成。")

    def explore_methods(self):
        hollows, ok = QInputDialog.getInt(self, "探索填补方法", "请输入空值数:")
        if not ok:
            return
        self.instruction_browser.setText("正在探索最佳填补方法……")
        for station_id in ID_LIST:
            input_filepath = f'Original_Data/{station_id}.xlsx'
            if os.path.exists(input_filepath):
                process_data(station_id, hollows, input_filepath)
            else:
                QMessageBox.warning(self, "File Not Found", f"{input_filepath} 不存在。")
        results = "\n".join([f"ID: {ID}, Min MSE: {min_mse}, Methods: {', '.join(methods)}"
                             for ID, (min_mse, methods) in min_mse_results.items()])
        self.load_images_from_directory(plot_explore)
        self.instruction_browser.append(f"探索结果:\n{results}")

    def fill_missing_data(self):
        self.instruction_browser.setText("请选择填补方法……")
        methods = {
            "Forward Fill": fill_forward,
            "Backward Fill": fill_backward,
            "Linear Interpolation": fill_linear,
            "KNN Imputation": fill_knn,
            "Seasonal Filling": fill_seasonal,
        }
        method, ok = QInputDialog.getItem(self, "数据填补", "选择方法:", list(methods.keys()), 0, False)
        if not ok:
            return
        chosen_method = methods[method]
        for station_id in ID_LIST:
            input_filepath = f'Original_Data/{station_id}.xlsx'
            output_filepath = os.path.join(FINAL_DATA_PATH, f"{station_id}-FilledData.xlsx")
            if os.path.exists(input_filepath):
                chosen_method(input_filepath, output_filepath, logger=self.log_message)
                plot_output_filepath = os.path.join(FINAL_PLOT_PATH, f"{station_id}-FilledComparison.png")
                plot_filled_data(input_filepath, output_filepath, plot_output_filepath, station_id)
            else:
                self.log_message(f"{input_filepath} 不存在。")
        self.load_images_from_directory(FINAL_PLOT_PATH)
        self.log_message("数据填补完成。")


# 启动应用
app = QApplication(sys.argv)
main_app = MainApp()
main_app.show()
sys.exit(app.exec_())