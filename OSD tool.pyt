#-*-coding :utf-8-*-
# @Author : Xin He
# @E-mail ：2938268503@qq.com
import arcpy, os,csv
import gjx as gj
import sys
import numpy as np
from math import sin, asin, cos, radians, fabs, sqrt
reload(sys)
sys.setdefaultencoding('utf-8') 

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the   .pyt file)."""
        self.label = "OSD Toolbox"
        self.alias = "Optimal demand-supply analysis"
        # List of tool classes associated with this toolbox
        self.tools = [Tool]

class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Optimal demand-supply analysis"
        self.description = "Optimal demand-supply analysis"
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

        fld_supply=arcpy.Parameter(name='supply_flds', displayName='Supply field', datatype='Field', direction='Input', parameterType='Required')
        fld_supply.parameterDependencies = [feas.name]
        fead=arcpy.Parameter(name='fead', displayName='Demand layer', datatype=['GPFeatureLayer','DETextfile'], direction='Input',parameterType='Required')

        fld_demand=arcpy.Parameter(name='demand_fld', displayName='Demand field', datatype='Field', direction='Input', parameterType='Required')
        fld_demand.parameterDependencies = [fead.name]
        dis_me=arcpy.Parameter(displayName="Distance calculation method", name="Distance calculation method", datatype="GPString",parameterType="Required", direction="Input")
        dis_me.filter.type = 'ValueList'
        dis_me.filter.list = ['Euclidean','Manhattan','Network']

        net_w=arcpy.Parameter(name='net_w', displayName='Neywork layers', datatype=['DENetworkDataset'], direction='Input',parameterType='Optional')
        outfile=arcpy.Parameter(name='outfile', displayName='Output table', datatype='DETextfile', direction='Output',parameterType='Required')
        outfile_ly=arcpy.Parameter(name='outfile_ly', displayName='Output layer', datatype='DEFeatureClass', direction='Output',parameterType='Required')
        net_me=arcpy.Parameter(displayName="Impedance_attribute", name="impedance_attribute", datatype="GPString",parameterType='Optional', direction="Input")
        net_me.filter.type = 'ValueList'
        net_me.filter.list = ['Length','Drivetime']
        return [feas,fld_supply,fead,fld_demand,dis_me,net_w,net_me,outfile,outfile_ly]

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
        def xy_point(x,y,prj):
            point = arcpy.Point(x,y)
            ptGeometry = arcpy.PointGeometry(point,prj)
            return ptGeometry

        def cal_Manh():
            dist_ij=[[999999.999 for x in range(supply_len)] for y in range(demand_len)]
            arcpy.AddMessage("Calculating...")
            if arcpy.Describe(fns).spatialReference.type=='Projected' and arcpy.Describe(fnd).spatialReference.type=='Projected':
                for i in range(demand_len):
                    for j in range(supply_len):
                        d3= (abs(datatable_d[i][1]-datatable_s[j][1])+ abs(datatable_d[i][2]-datatable_s[j][2]))
                        dist_ij[i][j]=d3
            elif arcpy.Describe(fns).spatialReference.type=='Geographic' and arcpy.Describe(fnd).spatialReference.type=='Geographic':
                ref_name=arcpy.Describe(fns).spatialReference.GCSCode
                sr = arcpy.SpatialReference(ref_name)
                for i in range(demand_len):
                    for j in range(supply_len):
                        point1=xy_point(datatable_d[i][1],datatable_d[i][2],sr)
                        point2=xy_point(datatable_d[i][1],datatable_s[j][2],sr)
                        point3=xy_point(datatable_s[j][1], datatable_s[j][2],sr)
                        d3=point1.angleAndDistanceTo(point2,"GEODESIC")[1]+point2.angleAndDistanceTo(point3,"GEODESIC")[1]  
                        dist_ij[i][j]=d3
            else:
                arcpy.AddMessage("Please unified the coordinate system")
            arcpy.AddMessage("OD Matrix calculation completed")
            return dist_ij
        def cal_Eu():
            dist_ij=[[999999.999 for x in range(supply_len)] for y in range(demand_len)]
            arcpy.AddMessage("Calculating...")
            if arcpy.Describe(fns).spatialReference.type=='Projected' and arcpy.Describe(fnd).spatialReference.type=='Projected':            
                for i in range(demand_len):
                    for j in range(supply_len):
                        d2=pow(datatable_d[i][1]-datatable_s[j][1],2)
                        d2+=pow(datatable_d[i][2]-datatable_s[j][2],2)
                        d3=pow(d2,0.5)
                        dist_ij[i][j]=d3
            elif arcpy.Describe(fns).spatialReference.type=='Geographic' and arcpy.Describe(fnd).spatialReference.type=='Geographic':
                ref_name=arcpy.Describe(fns).spatialReference.GCSCode
                sr = arcpy.SpatialReference(ref_name)          
                for i in range(demand_len):
                    for j in range(supply_len):
                        point1=xy_point(datatable_d[i][1],datatable_d[i][2],sr)
                        point2=xy_point(datatable_s[j][1], datatable_s[j][2],sr)
                        d3= point1.angleAndDistanceTo(point2,"GEODESIC")[1]
                        dist_ij[i][j]=d3

            else:
                arcpy.AddMessage("Please unified the coordinate system")                       

            arcpy.AddMessage("OD Matrix calculation completed")
            return dist_ij
        def cal_Net():
            try:

                arcpy.CheckOutExtension("Network")
            except:
                arcpy.AddMessage("Check whether the network analysis module is enabled")

            net_network = parameters[5].value
            net_m=parameters[6].valueAsText
            outNALayerName = 'ODMatrix_ly'
            if net_m=="Length":
                outNALayer = arcpy.na.MakeODCostMatrixLayer(net_network, outNALayerName, impedance_attribute="Length",UTurn_policy="ALLOW_UTURNS", hierarchy="NO_HIERARCHY",
                                                            output_path_shape="STRAIGHT_LINES")
            else:
                outNALayer = arcpy.na.MakeODCostMatrixLayer(net_network, outNALayerName, impedance_attribute="Drivetime",UTurn_policy="ALLOW_UTURNS", hierarchy="NO_HIERARCHY",
                                                            output_path_shape="STRAIGHT_LINES")
            outNALayer = outNALayer.getOutput(0)
            # Get the names of all the sublayers within the OD cost matrix layer.
            subLayerNames = arcpy.na.GetNAClassNames(outNALayer)

            # Stores the layer names that we will use later
            originsLayerName = subLayerNames["Origins"]
            destinationsLayerName = subLayerNames["Destinations"]
            arcpy.na.AddLocations(outNALayer, originsLayerName, fnd, sort_field='OBJECTID')
            arcpy.na.AddLocations(outNALayer, destinationsLayerName, fns, sort_field='OBJECTID')
            arcpy.na.Solve(outNALayer, "HALT")

            lry_list = arcpy.mapping.ListLayers(outNALayer)

            ODtable = []
            ODfiledname = []
            Lines = lry_list[4]
            rows = arcpy.SearchCursor(Lines)
            for row in rows:
                if net_m=="Length":
                    ods = [row.getValue("Name"), row.getValue("OriginID"), row.getValue("DestinationID"),
                       row.getValue("Total_Length")]
                else:
                    ods = [row.getValue("Name"), row.getValue("OriginID"), row.getValue("DestinationID"),
                       row.getValue("Total_Drivetime")]
                ODtable.append(ods)
            del rows, row

            ODtable = sorted(ODtable, key=(lambda x: [x[1], x[2]]))
            odarray = [i[3] for i in ODtable]
            odarray = np.array(odarray)
            supply_len = len(datatable_s)
            demand_len = len(datatable_d)

            dist_ij = odarray.reshape(demand_len, supply_len)

            arcpy.AddMessage("Calculating...")
            arcpy.AddMessage("OD Matrix calculation completed")

            return dist_ij


        fns=parameters[0].value #供给点要素

        sf=parameters[1].valueAsText #供给点，供给字段
        fnd=parameters[2].value #需求点要素

        df=parameters[3].valueAsText #需求点，需求字段

        dis_m=parameters[4].valueAsText
        outf=parameters[7].valueAsText

        outf_ly=parameters[8].valueAsText

        idx_s=0 #初始化供给点索引
        arcpy.AddMessage("Reading spatial units ...")
        #建立要素游标
        cursor_s = arcpy.SearchCursor(parameters[0].value)

        cursor_d = arcpy.SearchCursor(parameters[2].value)

        datatable_s=[] #供给点数据表
        datatable_d=[] #需求点数据表

        idx_d=0#初始化需求点索引
        supply_num=[] #初始化供给量
        demand_num=[]#初始化需求量
        id2idx_s={}
        id2idx_d={}

        for row_s in cursor_s:
            x_s,y_s=0,0#初始化X,Y坐标
            r_s=[idx_s,x_s,y_s,row_s.getValue(sf)]
            datatable_s.append(r_s)
            # row_s = cursor_s.next()
            idx_s+=1
        del cursor_s,row_s


        for row_d in cursor_d:
            x_d,y_d=0,0#初始化X,Y坐标
            r_d=[idx_d,x_d,y_d,row_d.getValue(df)]
            datatable_d.append(r_d)
            # row_d = cursor_d.next()
            idx_d+=1
        del cursor_d,row_d

        arcpy.env.overwriteOutput = True
        supply_len=len(datatable_s)
        demand_len=len(datatable_d)
        geometries_s = arcpy.CopyFeatures_management(fns, arcpy.Geometry())
        geometries_d = arcpy.CopyFeatures_management(fnd, arcpy.Geometry())
        for i in range(supply_len):
            cid_s=geometries_s[i].centroid
            datatable_s[i][1]=cid_s.X
            datatable_s[i][2]=cid_s.Y

        for i in range(demand_len):
            cid_d=geometries_d[i].centroid
            datatable_d[i][1]=cid_d.X
            datatable_d[i][2]=cid_d.Y

        arcpy.AddMessage("Calculating the OD...")
        if dis_m=="Euclidean": dist_ij=cal_Eu()
        if dis_m=='Manhattan': dist_ij=cal_Manh()
        if dis_m=="Network": dist_ij=cal_Net()
        arcpy.AddMessage("#")

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

        idr_list=[i[0] for i in results]
        ids_list=[i[0] for i in datatable_s]
        idd_list=[i[0] for i in datatable_d]

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

        
        return
