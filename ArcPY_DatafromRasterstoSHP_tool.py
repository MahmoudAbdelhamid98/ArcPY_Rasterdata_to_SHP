import arcpy
# we need the mapping module

from arcpy import mapping as mp
from arcpy import env
from arcpy import management as man
from arcpy import sa as spa 
env.overwriteOutput = True

# (1) GET INPUT
# Get trunks & BORHOLES & survey from the display

TrunkLayer = arcpy.GetParameter(0)
bhfname = arcpy.GetParameter(1)
surveyname = arcpy.GetParameter(2)
env.workspace = arcpy.GetParameter(3)
#workspace can be defined by user and the scratch work space will be the programs default to match all users
man.MakeXYEventLayer (bhfname ,"Eastimg", "Northing","BH_Layer")
man.MakeXYEventLayer (surveyname ,"E", "N","GL_Layer")

# (2) interpolate groundwater raster and Groundlevel from the boreholes and survey

GWraster = spa.Spline("BH_Layer.shp","GWT")
GLraster = spa.Spline("GL_Layer.shp","Z")

# (3) Add the requirred fields into the attribute table of trunks
fldlst = arcpy.ListFields(TrunkLayer)
cond = 0
for f in fldlst:
    if f.name == "h":
        cond = 1
if cond != 1:
    man.AddField(TrunkLayer, "h", "DOUBLE", 12, 2)
    
cond = 0
for f in fldlst:
    if f.name == "Qinf":
        cond = 1
if cond != 1:
    man.AddField(TrunkLayer, "Qinf", "DOUBLE", 12, 2)
    
cond = 0
for f in fldlst:
    if f.name == "PipeID":
        cond = 1
if cond != 1:
    man.AddField(TrunkLayer, "PipeID","TEXT","","",8)

cond = 0
for f in fldlst:
    if f.name == "USGL":
        cond = 1
if cond != 1:
    man.AddField(TrunkLayer, "USGL", "DOUBLE", 12, 2)

cond = 0
for f in fldlst:
    if f.name == "DSGL":
        cond = 1
if cond != 1:
    man.AddField(TrunkLayer, "DSGL", "DOUBLE", 12, 2)

man.CalculateField(TrunkLayer,"PipeID","\"P\"&( [FID] +1)")

# (4) create shapefile points at the middle, Start and End of trunks

man.FeatureVerticesToPoints(TrunkLayer,"USGL","START")
man.FeatureVerticesToPoints(TrunkLayer,"DSGL","END")
man.FeatureVerticesToPoints(TrunkLayer,"TrunkMidpt","MID")

# (5) use add surface uinformation to get gwl from raster into the midpoints

arcpy.AddSurfaceInformation_3d ("TrunkMidpt.shp", GWraster, "Z")
arcpy.AddSurfaceInformation_3d ("USGL.shp", GLraster, "Z")
arcpy.AddSurfaceInformation_3d ("DSGL.shp", GLraster, "Z")

# (6) join gwl between attributes

man.AddJoin(TrunkLayer,"PipeID","TrunkMidpt.shp","PipeID")
man.AddJoin(TrunkLayer,"PipeID","USGL.shp","PipeID")
man.AddJoin(TrunkLayer,"PipeID","DSGL.shp","PipeID")

#(7) calculate Q inf

man.CalculateField(TrunkLayer,"USGL","[USGL.Z]")
man.CalculateField(TrunkLayer,"DSGL","[DSGL.Z]")
man.CalculateField(TrunkLayer,"h","[TrunkMidpt.Z] -([trunks.USINV] + [trunks.DSINV])/2")
man.RemoveJoin(TrunkLayer)
man.SelectLayerByAttribute(TrunkLayer,"NEW_SELECTION","\"h\">0")
man.CalculateField(TrunkLayer,"Qinf","[Diameter]*0.001*0.001*[L]*([h]^(2/3))")
man.SelectLayerByAttribute(TrunkLayer,"CLEAR_SELECTION")

#Delete the stuff used throu the code (I took what I need already)

man.Delete(GWraster)
man.Delete(GLraster)
man.Delete("DSGL.shp")
man.Delete("USGL.shp")
man.Delete("TrunkMidpt.shp")
man.Delete("BH_Layer")
man.Delete("GL_Layer")



