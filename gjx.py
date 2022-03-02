# -*- coding: utf-8 -*-
import sys,os,random,time,copy,math
import arcpy
from pulp import *
reload(sys)
sys.setdefaultencoding('utf8')
global nodejs
#nodejs=[]
dataframe_s=[]
dataframe_d=[]
num_units=''
num_united=''
facilityCapacity =[] 
nodes=[]
def TP_model(nodejs):
    arcpy.AddMessage(str(nodejs))
    aa=os.getcwd()
    arcpy.AddMessage("num_units:"+aa)
    arcpy.AddMessage("nodes:"+str(len(nodes)))
    arcpy.AddMessage("num_unitd:"+str(num_united))
    arcpy.AddMessage("facilityCapacity:"+str(len(facilityCapacity)))
    # arcpy.AddMessage("##########:"+str(dataframe_s))
    import pulp
    try:
        prob = pulp.LpProblem("init_sdp",pulp.LpMinimize)#调用pulp
    except:
        prob = pulp.LpProblem("init_sdp",const.LpMinimize)#调用pulp
    variables = {}
    costs = {}
    arcpy.AddMessage("kkkkkkkkkk")
    arcpy.AddMessage(str(nodejs))
    arcpy.AddMessage("sssssssssss")
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
    current_path=os.getcwd()
    arcpy.AddMessage(current_path)
    cbc_path = "../cbc.exe"#cbc求解器的路径，也可指定为其他求解器
    cbc = COIN_CMD(path=cbc_path)
    #模型求解
    #初始化求解时间
    #time_start = time()
    prob.solve(cbc)
    #time_end = time()
    #tot_cost=str(time_end-time_start)#计算求解时间
    #teet= "*求解状态:"+str(LpStatus[prob.status])+"\n"+"*Total Cost of The Model ="+str(value(prob.objective))+"\n*模型求解时间为："+tot_cost
    if prob.status<0:
        arcpy.AddMessage("错误。求解失败，请重新核对数据")
    else:
        arcpy.AddMessage("解析并输出求解结果")
    # pass
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
    #return