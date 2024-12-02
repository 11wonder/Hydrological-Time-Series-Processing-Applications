# 水文时间序列处理应用  

基于Python的水文信号处理应用，包括趋势去除、异常值去除、滤波和填充方法以及数据填充操作。  
用户只需调用ui.py文件即可执行此程序。  
一、软件介绍  
1、 开发目的：  
开发针对水文时间序列的预处理软件，目的在于对所获取的复杂
且多样的水文时间序列数据进行系统、规范的处理，包括去除噪声、
填补缺失值、统一数据格式等操作，以提升数据质量，使其更准确、
完整且便于后续的分析、建模以及对水文规律的深入探究、水资源相
关决策的科学制定等应用。  
2、 主要功能：  
（1）水文时间序列文件读取  
（2）数据图像可视化  
（3）数据去趋势化处理  
（4）数据去除三倍标准差处理  
（5）数据去趋势化及去除三倍标准差处理  
（6）根据原始数列筛选出最优填补方式  
（7）选取填补方式对时间序列进行填补处理  
（8）存储填补数据结果  
（9）存储数据图像  
二．功能使用  
2.1 文件选取  
用户在 ![image](https://github.com/user-attachments/assets/680ed46b-5a12-4368-8a64-98e7f5e02b60)
文件夹中可以选择时间序列文件，如下图所示：
![image](https://github.com/user-attachments/assets/995d187a-0c8f-44ab-b9c9-00ac42f2dd3a)

打开 ![image](https://github.com/user-attachments/assets/2c6570b5-2c3f-4def-aef0-7ed6fa1c83bb)
文件夹后，可以看到不同的时间序列文件，用户可以
直接拖动需要处理的文件，如下图所示：
![image](https://github.com/user-attachments/assets/7a3cb3e8-e1a9-4ad1-a075-fea2c6ef9bb5)

针对水文时间序列的预处理软件 V1.0
4
2.2 程序使用
打开运行程序，本页面所展示的内容如图所示：
![image](https://github.com/user-attachments/assets/50f80010-ebd4-4d26-a979-68912296ab28)

图 1 首页
点击界面上方的 “![image](https://github.com/user-attachments/assets/8d338bf0-8c0e-4709-9be2-16f03ccc8b1a)
 ” 按钮，即可绘
针对水文时间序列的预处理软件 V1.0
5
制原始图像。其详情如下图所示：
![image](https://github.com/user-attachments/assets/095c7d07-4bb6-4336-acbc-ba5ef796cadf)

图 2 
用户选择第二个选项后，点击“ ![image](https://github.com/user-attachments/assets/d89c7080-da31-4c31-b3bc-860fd390ec57)
”按钮，可
以对图像进行去趋势处理，其中第一个按钮以及第三个按钮分别为不做处理以及
只去除三倍误差。如图所示：
![image](https://github.com/user-attachments/assets/12e939ff-ef55-4d5f-80ca-e826362c822b)

图 3
针对水文时间序列的预处理软件 V1.0
6
用户点击“![image](https://github.com/user-attachments/assets/1351ce21-318f-4b20-8504-102d2b5eaf5b)
 ”按钮，可以查看下一张图像，如
下图所示：
![image](https://github.com/user-attachments/assets/289de945-5d68-4fdc-a8fa-61203e3efd3b)

图 4 
用户选择第四个选项后，点击“![image](https://github.com/user-attachments/assets/df8c05c4-8a1a-460a-a38b-3e9c3b071002)
 ”按钮，可
以对图像进行进一步处理，为先进行去趋势化再进行去除误差，可以单独直接进
行，也可在第二个选项的基础上进行。如图所示：
![image](https://github.com/user-attachments/assets/056a01e5-10ee-41c0-aebd-222724bf8a89)

用户点击按钮可以探究填补方法，如下图所示：
![image](https://github.com/user-attachments/assets/ef7b3353-b5b9-4163-bbb2-457b432be1b7)

图 6 
空值数默认为 100，代表取一段延续的序列，随机挖取 100 个空，然后用
不同的方法进行填补，最后找出最优方法。如下图所示：
![image](https://github.com/user-attachments/assets/a09db076-0015-4f7c-8ef1-86dacb950678)

图 7
下图中第一列的图像为挖空后的原始图像，后 5 列图像为不同填补方法绘制后
的结果，如下图所示：
![image](https://github.com/user-attachments/assets/330daff0-bebf-4668-b47d-3400bafbb8b2)

图 8
用户可以选取不同的填补方法，如下图所示：
![image](https://github.com/user-attachments/assets/196c1cf9-6bed-4c29-a530-4aad030477e1)

![image](https://github.com/user-attachments/assets/906079be-d7a1-4887-932f-dc03db3e6f10)

图 9
2.3 图像文件保存
针对水文时间序列的预处理软件 V1.0
![image](https://github.com/user-attachments/assets/4e38449b-00d9-4964-84f9-394ae381166c)

10
Original_Data_Plotting 中储存了初始数据绘图后的图像
![image](https://github.com/user-attachments/assets/dbaf9353-8f19-4001-a280-69695ad3805d)

detrend_data 中储存了只进行去趋势化后的数据
![image](https://github.com/user-attachments/assets/bae5d82e-2d5c-41ba-a89b-0d3e74761843)

针对水文时间序列的预处理软件 V1.0
11
detrend_plotting 中储存了只进行去趋势化后的数据绘图
![image](https://github.com/user-attachments/assets/f69f3ced-78ea-4401-bd55-9860a50b2de4)

threshold_data 中储存了只去除三倍标准差后的数据（如果先进行趋势再进行去除三倍标准
![image](https://github.com/user-attachments/assets/9e7cec48-a696-4596-8e4a-85314f31d0a0)

差，即二者都进行，数据也保存在这个文件夹中）
threshold_plotting 中储存了只去除三倍标准差后的数据绘图
![image](https://github.com/user-attachments/assets/ea672b31-1239-4296-bab9-a53f4ee78046)

detrend_removeoutliers_plotting 中储存了先进行去除趋势再去除三倍标准差的数据绘图
![image](https://github.com/user-attachments/assets/89a4db74-cfb8-4ccc-8184-ddf4a7a61fc3)

针对水文时间序列的预处理软件 V1.0
12
Explore completion methods 中储存了五种方法填充后的效果，并计算 MSE
![image](https://github.com/user-attachments/assets/cea6349c-f80e-4f75-8bf6-d18b8f36a18b)

Final data filling 中储存了用户选择填补方法后的填补数据结果
![image](https://github.com/user-attachments/assets/e24694dd-314b-48e2-bcbe-661a9073b05e)

Complete and compare the plotting 中储存了填补后的可视化结果
![image](https://github.com/user-attachments/assets/7f9c8f6b-ca00-4124-92c2-7d2ebd30a7e3)
