# -*- coding: utf-8 -*-
import sys,os,random,time,copy,math
import arcpy
from pulp import *
reload(sys)
sys.setdefaultencoding('utf8')

dataframe_s=[]
dataframe_d=[]
num_units=''
num_united=''
facilityCapacity =[] 
nodes=[]
def TP_model(nodejs):

    aa=os.getcwd()

    import pulp
    try:
        prob = pulp.LpProblem("init_sdp",pulp.LpMinimize)#调用pulp
    except:
        prob = pulp.LpProblem("init_sdp",const.LpMinimize)#调用pulp
    variables = {}
    costs = {}

    for i in range(num_united):
        for j in range(num_units):
            variables["x_" +str(i)+ "_"+ str(j)]=pulp.LpVariable("x_" +str(i)+ "_"+ str(j), 0, None, pulp.LpInteger) #
            cost=nodejs[i][j] 
            costs["x_" +str(i)+ "_"+ str(j)]=cost
    obj = 0
    # 计算所有需求点到所有供给点的总成本
    for x in variables:
        obj += costs[x] * variables[x]
    prob += obj
    #对于每个需求点来说，被服务的人口之和要等于需求点总人口
    for i in range(num_united):
        s = 0
        for j in range(num_units):
            s += variables["x_" + str(i) + "_" + str(j)]
        prob += s == nodes[i]
    for k in range(num_units):
        s = 0
        for i in range(num_united):
            s += variables["x_" + str(i) + "_" + str(k)]
        prob += s <= facilityCapacity[k]


    cbc = COIN_CMD()

    #模型求解
    #初始化求解时间
    prob.solve(cbc)

    if prob.status<0:
        arcpy.AddMessage("错误。求解失败，请重新核对数据")
    else:
        arcpy.AddMessage("解析并输出求解结果")

        assignsum = 0
        list_c = []
        for v in prob.variables():
            if v.varValue > 0:
                list_r = []
                items = v.name.split('_')
                i = int(items[1])
                k = int(items[2])
                dis=nodejs[i][k]
                assign = v.varValue
                list_r.append(i)
                list_r.append(k)
                list_r.append(assign)
                list_r.append(dis)
                list_c.append(list_r)
    return list_c
