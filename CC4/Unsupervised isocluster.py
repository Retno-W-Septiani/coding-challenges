import arcpy
from arcpy.sa import *
arcpy.env.workspace = r"C:\Users\Wulan\Documents\Phd\Spring 2022\NRS528\CC4"  # change the directory here
arcpy.env.overwriteOutput = True  # to prevent error due to 'file already exist'

# Set local variables
inRaster = "RI_spring2021.tif"  # targeted raster
classes = 5  # class number being created
minMembers = 50
sampInterval = 15

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# Execute IsoCluster
outUnsupervised = IsoClusterUnsupervisedClassification(inRaster, classes, minMembers, sampInterval)
outUnsupervised.save(r"C:\Users\Wulan\Documents\Phd\Spring 2022\NRS528\CC4\result.tif")  # change path and
                                                                                            # file name before .tif
