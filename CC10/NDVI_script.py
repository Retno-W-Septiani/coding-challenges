# # # This is Coding Challenge 10
# # # Retno Wulan Septiani , April 2022

# # In this coding challenge, NDVI was generated using Raster Calculator
# # NDVI is calculated from the visible and near-infrared light reflected by vegetation.
# Healthy vegetation absorbs most of the visible light that hits it,
# and reflects a large portion of the near-infrared light.

# # To generate NDVI from a multi-spectral data
# check out: https://pro.arcgis.com/en/pro-app/latest/arcpy/image-analyst/ndvi.htm


import os
import arcpy

arcpy.env.overwriteOutput = True

data_directory = r'C:\Users\Wulan\Documents\Phd\Spring 2022\NRS528\coding-challenges\CC10\Landsat_data'
list_input = os.listdir(data_directory)
print("Folder available: " + str(list_input))

for data in list_input:
    arcpy.env.workspace = data_directory + '/' + str(data)
    list_raster = arcpy.ListRasters("*", "TIF")
    print("Gathering all Raster files in " + str(arcpy.env.workspace) + ".......")
    print("Searching for Band 4 and Band 5.....")
    NDVI = arcpy.sa.RasterCalculator([[x for x in list_raster if "B4" in x], [x for x in list_raster if "B5" in x]], ['x', 'y'], '(y-x)/(y+x)')
    print("Calculating NDVI...")
    saveraster = NDVI.save("output" + data + ".tif")
    if arcpy.Exists("output" + data + ".tif"):
        print("NDVI Calculated Successfully for " + "output" + data + ".tif")



