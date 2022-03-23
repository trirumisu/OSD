# Optimal demand-supply analysis
ArcGIS Python Toolbox for Optimal demand-supply analysis.

![Note](https://i.imgur.com/Ic8BA7C.png) **重要提示:** 该工具箱仅支持 **ArcGIS 10.2及以上**。
* 作者: 孔云峰 (<https://github.com/yfkong>) | 翟石艳 (zsycenu@hotmail.com)

**目录**

1. [说明](#说明)
2. [安装](#安装)




## 说明
**Optimal demand-supply analysis** 是 **最优供需分配模型** 的 ArcGIS Python Toolbox,是孔云峰教授和翟石艳副教授提出新的最优供需分配的公共设施空间可达性计算方法([文章](DOI: 10.11821/dlxb20220)。该工具基于最优供需分配模型，将设施服务分配给需求者，根据分配结果计算空间可达性指标。给定服务设施与需求的空间分布，以最小化旅行成本为目标，顾及设施服务能力，采用经典的运输问题模型确定最优的服务供需分配方案，进而度量服务的空间可达性。该方法方法无需参数，计算高效，结果易于解释，在公共服务评价及设施布局规划方面具有应用潜力。
## 安装
### Step 1: 下载工具
1. 点击页面右上角的绿色按钮下载 (**[Clone or download](https://github.com/trirumisu/OSD/archive/refs/heads/main.zip)**) 该工具的压缩包。
2. 解压压缩文件至本地，将所有文件复制到文件目录中。

### Step 2: 环境设置

将 **cbc.exe所在路径** 设置到系统变量path中。

### Step 3: 安装PuLP
安装PuLP 2.5.1 (https://pypi.org/project/PuLP/) (推荐但不是必须)。

### Step 4: 连接工具箱
在ArcGIS中，导航到文件目录，单击工具。 

## 工具使用及结果
### Step 1: 打开工具

### Step 2: 输入数据

### Step 3: 运行工具，输出结果

## 支持数据格式
* 供给点数据（必选）:
* 需求点数据（必选）:
* 路网数据（可选）:

## 授权
* 该工具为开源工具，仅供学习交流
* 如果您使用此工具用于您的研究，请引用我们的文章（DOI: 10.11821/dlxb20220）
## 报告错误


