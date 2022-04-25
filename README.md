# Optimal demand-supply analysis
ArcGIS Python Toolbox for Optimal demand-supply analysis.

![Note](https://i.imgur.com/Ic8BA7C.png) **重要提示:** 该工具箱仅支持 **ArcGIS 10.3及以上**。
* 代码贡献者：何新新 (2938268503@qq.com) | 罗静静 (ljj18238220679@126.com)
* 文章作者:  翟石艳 (zsycenu@hotmail.com) | 何新新 (2938268503@qq.com)<br>
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;孔云峰* (<https://github.com/yfkong>)  | 罗静静 (ljj18238220679@126.com)  
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;宋根鑫 (shengliking@126.com)


**目录**

1. [说明](#说明)
2. [安装](#安装)
3. [数据准备](#数据准备)
4. [工具使用及结果](#工具使用及结果)
5. [授权](#授权)
6. [报告错误](#报告错误)





## 说明
**Optimal demand-supply analysis** 模型和工具可用于公共设施空间可达性计算，由孔云峰教授和翟石艳副教授提出(2022)。该工具基于Python语言和ArcGIS10.3及以上平台运行。该方法的基本原理为，给定服务设施与需求的空间分布，以最小化旅行成本为目标，顾及设施服务能力，采用经典的运输问题模型确定最优的服务供需分配方案，进而计算服务的空间可达性指标。该方法无需参数，计算高效，结果易于解释，在公共服务评价及设施布局规划方面具有应用潜力。该方法的详细表述和案例分析见文章(翟石艳，何新新，孔云峰*，罗静静，宋根鑫.基于最优供需分配的公共设施空间可达性分析[J],地理学报，2022,77（4）：1-12. DOI: 10.11821/dlxb20220)。

## 安装
### Step 1: 下载工具
1. 点击页面右上角的绿色按钮下载 (**[Clone or download](https://github.com/trirumisu/OSD/archive/refs/heads/main.zip)**) 该工具的压缩包。
2. 解压压缩文件至本地，将所有文件复制到同一文件目录中。

### Step 2: 环境设置

将 **cbc.exe所在路径** 设置到系统变量path中。

### Step 3: 安装PuLP
安装PuLP 2.5.1 (https://pypi.org/project/PuLP/) (推荐但不是必须)。

### Step 4: 连接工具箱
在ArcGIS中，导航到文件目录，单击工具。 

## 数据准备
准备**供给点数据**（Shapefile或文件地理数据库要素类）、**需求点数据**（Shapefile或文件地理数据库要素类）、**路网数据**（可选）（网络数据集）。
其中供给点数据需包含供给点数量字段、需求点数据需包含需求数据量字段。网络数据集的具体构建见：https://desktop.arcgis.com/zh-cn/arcmap/latest/extensions/network-analyst/exercise-1-creating-a-network-dataset.html

![daytype](https://github.com/trirumisu/OSD/blob/main/data.png)

* 注意：
在构建网络数据集时，若以距离为阻抗成本应将属性名称重命名为**Length**，若以驾驶时间为阻抗成本应将属性名称重命名为**Drivetime**。
![note](https://github.com/trirumisu/OSD/blob/main/note.png)

## 工具使用及结果
### Step 1: 打开工具
![interface](https://github.com/trirumisu/OSD/blob/main/interface.png)

### Step 2: 输入数据
![input](https://github.com/trirumisu/OSD/blob/main/input.png)

### Step 3: 运行工具，输出结果

![run](https://github.com/trirumisu/OSD/blob/main/run.png)
![result1](https://github.com/trirumisu/OSD/blob/main/result1.png)
![result2](https://github.com/trirumisu/OSD/blob/main/result2.png)

## 授权
* 该工具为开源工具，仅供学习交流。
* 若使用此工具用于您的工作和学术研究，请引用我们的文章
* 翟石艳，何新新，孔云峰*，罗静静，宋根鑫.基于最优供需分配的公共设施空间可达性分析[J],地理学报，2022,77（4）：1-12. DOI: 10.11821/dlxb20220

## 报告错误
如果您遇到软件缺陷(即bug)，请报告该问题。请联系2938268503@qq.com

