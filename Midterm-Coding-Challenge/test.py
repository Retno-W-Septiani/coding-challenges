import arcpy
import csv
file = open('firestations.csv', "r")
csv_reader = csv.reader(file)
# # #  converting csv into a shp file
in_Table = 'firestations.csv'
x_coords = "x"
y_coords = "y"
z_coords = ""
out_Layer = 'variables'
saved_Layer = 'fs.shp'
spRef = arcpy.SpatialReference(4326)  # # setting the spatial reference where 4326 == WGS 1984
# # system is creating the shp file
lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)
# # saving the shp file
arcpy.CopyFeatures_management(lyr, saved_Layer)
if arcpy.Exists(saved_Layer):
    print("CSV files converted successfully!")