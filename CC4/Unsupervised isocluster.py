# # # This is Unsupervised classification - iso cluster tool which is a tool
# # that automatically finds the clusters in an image and outputs a classified image.
# # In this case, the users do not need to determine any class sample, signature files or training
# # because all work is done by the computer.

# # # Retno Septiani (March,2022)


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
outUnsupervised.save(r"result.tif")  # change file name before .tif
