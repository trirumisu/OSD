#-*-coding :utf-8-*-
import arcpy, os,csv
import gjx as gj
import sys
import numpy as np
reload(sys)
sys.setdefaultencoding('utf-8') 

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the   .pyt file)."""
        self.label = "OSD Toolbox"
        self.alias = "Reassign the service between facilities and communities"
        # List of tool classes associated with this toolbox
        self.tools = [Tool]

class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Reassign the service between facilities and communities"
        self.description = "Reassign the service between facilities and communities"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        """
        feas:供给点图层
        fld_ids:供给点ID
        fld_supply:供给数量
        fead:需求点图层
        fld_idd:需求点ID
        fld_num:需求点数量
        """
        feas=arcpy.Parameter(name='feas', displayName='Supply layer', datatype=['GPFeatureLayer','DETextfile'], direction='Input',parameterType='Required')
        # fld_ids=arcpy.Parameter(name='id_flds', displayName='sID field', datatype='Field', direction='Input', parameterType='Required')
        # fld_ids.parameterDependencies = [feas.name]
        fld_supply=arcpy.Parameter(name='supply_flds', displayName='Supply field', datatype='Field', direction='Input', parameterType='Required')
        fld_supply.parameterDependencies = [feas.name]
        fead=arcpy.Parameter(name='fead', displayName='Demand layer', datatype=['GPFeatureLayer','DETextfile'], direction='Input',parameterType='Required')
        # fld_idd=arcpy.Parameter(name='id_fldd', displayName='dID field', datatype='Field', direction='Input', parameterType='Required')
        # fld_idd.parameterDependencies = [fead.name]
        fld_demand=arcpy.Parameter(name='demand_fld', displayName='Demand field', datatype='Field', direction='Input', parameterType='Required')
        fld_demand.parameterDependencies = [fead.name]
        dis_me=arcpy.Parameter(displayName="Distance calculation method", name="Distance calculation method", datatype="GPString",parameterType="Required", direction="Input")
        dis_me.filter.type = 'ValueList'
        dis_me.filter.list = ['Euclidean','Manhattan','Network']
        net_w=arcpy.Parameter(name='net_w', displayName='Neywork layers', datatype=['DENetworkDataset'], direction='Input',parameterType='Optional')
        outfile=arcpy.Parameter(name='outfile', displayName='Output table', datatype='DETextfile', direction='Output',parameterType='Required')
        outfile_ly=arcpy.Parameter(name='outfile_ly', displayName='Output layer', datatype='DEFeatureClass', direction='Output',parameterType='Required')
        # fld_id=arcpy.Parameter(name='id_fld', displayName='ID field', datatype='Field', direction='Input', parameterType='Required')
        return [feas,fld_supply,fead,fld_demand,dis_me,net_w,outfile,outfile_ly]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return
    def execute(self, parameters, messages):
        """The source code of the tool."""
        if arcpy.env.workspace==None:
             arcpy.AddMessage("please set the workspace! 'Geoprocessing'->'Envronments.'")		
             return
        def cal_Manh():
            arcpy.AddMessage("Manh...")
            arcpy.AddMessage(str(demand_len))
            arcpy.AddMessage(str(supply_len))
            dist_ij=[[999999.999 for x in range(supply_len)] for y in range(demand_len)]
            arcpy.AddMessage(str(dist_ij))
            for i in range(demand_len):
                for j in range(supply_len):
                    d3= (abs(datatable_d[i][1]-datatable_s[j][1])+ abs(datatable_d[i][2]-datatable_s[j][2]))/1000
                    dist_ij[i][j]=d3
                    arcpy.AddMessage("calculating...")
            arcpy.AddMessage(str(dist_ij))
            arcpy.AddMessage("OD Matrix calculation completed")
            return dist_ij
        def cal_Eu():
            arcpy.AddMessage("Eu_dis...")
            arcpy.AddMessage(str(demand_len))
            arcpy.AddMessage(str(supply_len))
            dist_ij=[[999999.999 for x in range(supply_len)] for y in range(demand_len)]
            arcpy.AddMessage(str(dist_ij))
            for i in range(demand_len):
                for j in range(supply_len):
                    d2=pow(datatable_d[i][1]-datatable_s[j][1],2)
                    d2+=pow(datatable_d[i][2]-datatable_s[j][2],2)
                    d3=pow(d2,0.5)/1000
                    arcpy.AddMessage("calculating...")
                    dist_ij[i][j]=d3
            arcpy.AddMessage(str(dist_ij))
            arcpy.AddMessage("OD Matrix calculation completed")
            return dist_ij
        def cal_Net():
            arcpy.AddMessage("Net...")
            if arcpy.CheckExtension("Network") == "Available":
                arcpy.CheckOutExtension("Network")
            else:
             # Raise a custom exception
                net_network=parameters[5].value
                outNALayerName='ODMatrix_ly'
                outNALayer = arcpy.na.MakeODCostMatrixLayer(net_network, outNALayerName,impedance_attribute="Length", UTurn_policy="ALLOW_UTURNS",hierarchy="NO_HIERARCHY",output_path_shape="STRAIGHT_LINES")
                outNALayer = outNALayer.getOutput(0)
                #Get the names of all the sublayers within the OD cost matrix layer.
                subLayerNames = arcpy.na.GetNAClassNames(outNALayer)
                arcpy.AddMessage(str(subLayerNames))
                #Stores the layer names that we will use later
                originsLayerName = subLayerNames["Origins"]
                destinationsLayerName = subLayerNames["Destinations"]
                arcpy.na.AddLocations(outNALayer, originsLayerName,fnd,sort_field = 'OBJECTID')
                arcpy.na.AddLocations(outNALayer, destinationsLayerName,fns,sort_field = 'OBJECTID')
                arcpy.na.Solve(outNALayer,"HALT")  
                # desc = arcpy.Describe(outNALayer)
                lry_list=arcpy.mapping.ListLayers(outNALayer)
                outLayerFile = "C:/Users/hp/Desktop/" + "/" + outNALayerName + ".lyr"
                arcpy.management.SaveToLayerFile(outNALayer,outLayerFile,"RELATIVE")
                ODtable=[]
                for i in lry_list:
                    if i.name=='Lines':
                        arcpy.AddMessage(i.name)
                        rows = arcpy.SearchCursor(i)
                        for row in rows:
                            ods=[row.getValue("Name"),row.getValue("OriginID"),row.getValue("DestinationID"),row.getValue("Total_Length")]
                            ODtable.append(ods)
                        del rows,row
                ODtable=sorted(ODtable,key=(lambda x:[x[1],x[2]]))
                odarray=[i[3] for i in ODtable]
                odarray=np.array(odarray)
                supply_len=len(datatable_s)
                demand_len=len(datatable_d)
                dist_ij=odarray.reshape(demand_len,supply_len)
                arcpy.AddMessage(str(odarray.shape))
                arcpy.AddMessage(str(odarray))
                arcpy.AddMessage("OD Matrix calculation completed")
                # f = open(outf,'wb')
                # # # filed_name=["Name","OriginID","DestinationID","Total_Length"]
                # writer = csv.writer(f)
                # # writer.writerow(filed_name)
                # for i in odarray:
                #     writer.writerow(i)
                # f.close()
            return dist_ij
        global idf
        global sf
        global idd
        global df
        fns=parameters[0].value #供给点要素
        # global ids
        # ids=parameters[1].valueAsText #供给点，ID字段
        sf=parameters[1].valueAsText #供给点，供给字段
        fnd=parameters[2].value #需求点要素
        # idd=parameters[4].valueAsText #需求点，ID字段
        df=parameters[3].valueAsText #需求点，需求字段
        global outf
        global dis_m
        dis_m=parameters[4].valueAsText
        outf=parameters[6].valueAsText
        global outf_ly
        outf_ly=parameters[7].valueAsText
        global idx_s
        idx_s=0 #初始化供给点索引
        arcpy.AddMessage("reading spatial units ...")
        #建立要素游标
        cursor_s = arcpy.SearchCursor(parameters[0].value)
        # row_s = cursor_s.next()#迭代
        cursor_d = arcpy.SearchCursor(parameters[2].value)
        # row_d = cursor_d.next()#迭代
        datatable_s=[] #供给点数据表
        datatable_d=[] #需求点数据表
        global idx_d
        idx_d=0#初始化需求点索引
        supply_num=[] #初始化供给量
        demand_num=[]#初始化需求量
        id2idx_s={}
        id2idx_d={}
        # while row_s :
        for row_s in cursor_s:
            x_s,y_s=0,0#初始化X,Y坐标
            r_s=[idx_s,x_s,y_s,row_s.getValue(sf)]
            datatable_s.append(r_s)
            # row_s = cursor_s.next()
            idx_s+=1
        del cursor_s,row_s
        arcpy.AddMessage(str(datatable_s))
        # while row_d :
        for row_d in cursor_d:
            x_d,y_d=0,0#初始化X,Y坐标
            r_d=[idx_d,x_d,y_d,row_d.getValue(df)]
            datatable_d.append(r_d)
            # row_d = cursor_d.next()
            idx_d+=1
        del cursor_d,row_d
        arcpy.AddMessage(str(datatable_d))
        arcpy.env.overwriteOutput = True
        supply_len=len(datatable_s)
        demand_len=len(datatable_d)
        geometries_s = arcpy.CopyFeatures_management(fns, arcpy.Geometry())
        geometries_d = arcpy.CopyFeatures_management(fnd, arcpy.Geometry())
        for i in range(supply_len):
            cid_s=geometries_s[i].centroid
            datatable_s[i][1]=cid_s.X
            datatable_s[i][2]=cid_s.Y
        arcpy.AddMessage("total units: "+str(datatable_s))
        for i in range(demand_len):
            cid_d=geometries_d[i].centroid
            datatable_d[i][1]=cid_d.X
            datatable_d[i][2]=cid_d.Y
        arcpy.AddMessage("total units: "+str(datatable_d))
        arcpy.AddMessage("Calculating the OD...")
        if dis_m=="Euclidean": dist_ij=cal_Eu()
        if dis_m=='Manhattan': dist_ij=cal_Manh()
        if dis_m=="Network": dist_ij=cal_Net()
        arcpy.AddMessage("#")
        arcpy.AddMessage(str(dist_ij))
        arcpy.SetProgressorLabel("Solving the problem......")
        arcpy.AddMessage("Solving the problem......")
        #调用pulp建立模型并求解
        #gj.nodejs=dist_ij
        gj.dataframe_s=datatable_s
        gj.dataframe_d=datatable_d
        gj.num_units=supply_len
        gj.num_united=demand_len
        gj.facilityCapacity=[i[3] for i in datatable_s]
        gj.nodes=[i[3] for i in datatable_d]
        results=gj.TP_model(dist_ij)
        arcpy.AddMessage("The problem has been sovled......")
        #arcpy.AddMessage(str(results))
        idr_list=[i[0] for i in results]
        ids_list=[i[0] for i in datatable_s]
        idd_list=[i[0] for i in datatable_d]
        arcpy.AddMessage(str(len(results)))
        arcpy.AddMessage(str(idr_list))
        num=0
        for i in results:
            i.append(datatable_d[idd_list.index(i[0])][1])
            i.append(datatable_d[idd_list.index(i[0])][2])
            i.append(datatable_s[ids_list.index(i[1])][1])
            i.append(datatable_s[ids_list.index(i[1])][2])
            num+=1
        arcpy.SetProgressorLabel("Outputing the results......")
        arcpy.AddMessage("Outputing the results......")
        f = open(outf,'wb')
        filed_name=["i","k","assign","dis","i_X","i_Y","k_X","k_Y"]
        writer = csv.writer(f)
        writer.writerow(filed_name)
        for i in results:
            writer.writerow(i)
        f.close()
        arcpy.AddMessage('XYToLine...')
        arcpy.XYToLine_management(outf,outf_ly,
                         "i_X","i_Y","k_X",
                         "k_Y","GEODESIC","dis")
        # # arcpy.AddMessage(str(results))
        # # arcpy.AddMessage(str(num))
        # # idf1=parameters[0].valueAsText
        # # b = [i[0] for i in a]     # 从a中的每一行取第一个元素。
        # # # idf2=parameters[1].valueAsText
        # # cursor = arcpy.SearchCursor(parameters[0].value)
        # # row = cursor.next()
        # # i=0
        # # while row:
        # #     i+=1
        # #     row = cursor.next()
        
        return
